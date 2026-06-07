"""Knowledge graph subgraph query tool."""

import logging
import traceback
from typing import Annotated, Any

from langchain.tools import tool

from src.knowledge.adapters.base import BaseNeo4jAdapter

logger = logging.getLogger(__name__)

SUBGRAPH_QUERY_DESCRIPTION = """
查询知识图谱子图工具。当用户询问实体关系、知识图谱相关内容时，使用此工具查询。
输入关键词，返回该实体周围的知识子图（包含节点和关系），结果会在对话中展示为可视化图谱卡片。
参数 hops 控制子图扩展深度（默认2），增加跳数以发现更多间接关联的实体。
"""


def _add_node(nodes: dict, neo4j_node) -> str:
    """Add a Neo4j node to the nodes dict, return its element_id."""
    nid = neo4j_node.element_id
    if nid not in nodes:
        name = dict(neo4j_node).get("name") or dict(neo4j_node).get("entity_id") or ""
        nodes[nid] = {"id": nid, "name": name, "labels": list(neo4j_node.labels)}
    return nid


def _add_edge(edges: list, rel, source_id: str, target_id: str, seen: set) -> None:
    """Add an edge if not already seen."""
    rel_type = dict(rel).get("keywords") or rel.type
    key = (source_id, target_id, rel_type)
    if key not in seen:
        seen.add(key)
        edges.append({
            "id": rel.element_id,
            "source_id": source_id,
            "target_id": target_id,
            "type": rel_type,
        })


@tool(
    name_or_callable="query_subgraph",
    description=SUBGRAPH_QUERY_DESCRIPTION,
)
def query_subgraph(
    query: Annotated[str, "查询关键词，用于搜索知识图谱中的实体"],
    max_entities: Annotated[int, "返回的最大实体数量，默认50"] = 50,
    hops: Annotated[int, "子图扩展跳数，默认2"] = 2,
) -> Any:
    """从知识库（Neo4j）中查询知识图谱子图，返回节点和关系数据。

    直接通过 Cypher 查询 Neo4j 中所有知识库 (kb_*) 构建的图谱数据，
    支持多跳扩展返回关联的子图，返回前端可渲染的 nodes + edges + triples 格式。

    Args:
        query: 查询关键词
        max_entities: 返回的最大实体数量
        hops: 子图扩展跳数

    Returns:
        包含 nodes, edges, triples 的知识子图数据
    """
    try:
        logger.debug(f"Querying knowledge base subgraph with: query={query}, max_entities={max_entities}, hops={hops}")

        adapter = BaseNeo4jAdapter()
        nodes: dict[str, dict] = {}
        edges: list[dict] = []
        seen_edges: set[tuple] = set()
        hops = max(1, min(hops, 3))  # Clamp 1-3

        with adapter.driver.session() as session:

            # Step 1: Find seed nodes
            seed_results = session.execute_read(
                lambda tx, kw, lim: list(tx.run("""
                    MATCH (n)
                    WHERE any(label IN labels(n) WHERE label STARTS WITH 'kb_')
                      AND (toLower(n.name) CONTAINS toLower($kw)
                           OR toLower(n.entity_id) CONTAINS toLower($kw))
                    RETURN n
                    LIMIT $lim
                """, kw=query, lim=max_entities)),
                query, max_entities,
            )
            frontier: list[str] = []
            for record in seed_results:
                nid = _add_node(nodes, record["n"])
                frontier.append(nid)

            if not frontier:
                return {"nodes": [], "edges": [], "triples": []}

            # Step 2: Multi-hop expansion
            for _ in range(hops):
                if not frontier:
                    break
                expand_results = session.execute_read(
                    lambda tx, fids: list(tx.run("""
                        MATCH (n)
                        WHERE elementId(n) IN $fids
                        OPTIONAL MATCH (n)-[r]-(m)
                        WHERE any(label IN labels(m) WHERE label STARTS WITH 'kb_')
                        RETURN n, r, m
                    """, fids=fids)),
                    frontier,
                )
                frontier = []
                for record in expand_results:
                    n_node = record.get("n")
                    r_rel = record.get("r")
                    m_node = record.get("m")

                    if n_node:
                        _add_node(nodes, n_node)
                    if m_node:
                        mid = _add_node(nodes, m_node)
                        if mid not in [nodes[n]["id"] for n in frontier]:  # Simple check
                            frontier.append(mid)
                    if r_rel and n_node and m_node:
                        _add_edge(edges, r_rel, n_node.element_id, m_node.element_id, seen_edges)

                # Deduplicate frontier
                frontier = list(dict.fromkeys(frontier))

        result_nodes = list(nodes.values())
        node_map = {n["id"]: n["name"] for n in result_nodes}
        triples = []
        for e in edges:
            src = node_map.get(e["source_id"], e["source_id"])
            tgt = node_map.get(e["target_id"], e["target_id"])
            triples.append([src, e["type"], tgt])

        logger.debug(f"Subgraph query returned {len(result_nodes)} nodes, {len(edges)} edges")
        return {"nodes": result_nodes, "edges": edges, "triples": triples}

    except Exception as e:
        logger.error(f"Subgraph query error: {e}, {traceback.format_exc()}")
        return {"nodes": [], "edges": [], "triples": [], "error": str(e)}
