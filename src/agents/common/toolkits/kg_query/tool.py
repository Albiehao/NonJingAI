"""Knowledge graph query tool."""

import logging
import traceback
from typing import Annotated, Any

from langchain.tools import tool

from src.knowledge.adapters.base import BaseNeo4jAdapter

logger = logging.getLogger(__name__)

KG_QUERY_DESCRIPTION = """
使用这个工具可以查询知识图谱中包含的三元组信息。
关键词（query），使用可能帮助回答这个问题的关键词进行查询，不要直接使用用户的原始输入去查询。
"""


@tool(name_or_callable="query_knowledge_graph", description=KG_QUERY_DESCRIPTION)
def query_knowledge_graph(query: Annotated[str, "The keyword to query knowledge graph."]) -> Any:
    """查询知识图谱中包含的三元组信息。

    直接查询 Neo4j 中所有知识库 (kb_*) 构建的图谱数据，返回三元组列表。

    Args:
        query: 查询关键词，应使用可能帮助回答问题的关键词，而非用户原始输入

    Returns:
        知识图谱查询结果，包含三元组信息
    """
    try:
        logger.debug(f"Querying knowledge graph with: {query}")

        adapter = BaseNeo4jAdapter()
        triples = []
        seen = set()

        def search_triples(tx, keyword):
            q = """
            MATCH (n)
            WHERE any(label IN labels(n) WHERE label STARTS WITH 'kb_')
              AND (toLower(n.name) CONTAINS toLower($keyword)
                   OR toLower(n.entity_id) CONTAINS toLower($keyword))
            OPTIONAL MATCH (n)-[r]-(m)
            WHERE any(label IN labels(m) WHERE label STARTS WITH 'kb_')
            RETURN n, r, m
            LIMIT 100
            """
            return list(tx.run(q, keyword=keyword))

        with adapter.driver.session() as session:
            records = session.execute_read(search_triples, query)
            node_names = {}

            for record in records:
                n_node = record.get("n")
                if n_node:
                    nid = n_node.element_id
                    if nid not in node_names:
                        node_names[nid] = dict(n_node).get("name") or dict(n_node).get("entity_id") or nid

                m_node = record.get("m")
                if m_node:
                    mid = m_node.element_id
                    if mid not in node_names:
                        node_names[mid] = dict(m_node).get("name") or dict(m_node).get("entity_id") or mid

                r_rel = record.get("r")
                if r_rel and n_node and m_node:
                    rel_type = dict(r_rel).get("keywords") or r_rel.type
                    key = (n_node.element_id, m_node.element_id, rel_type)
                    if key not in seen:
                        seen.add(key)
                        src_name = node_names.get(n_node.element_id, n_node.element_id)
                        tgt_name = node_names.get(m_node.element_id, m_node.element_id)
                        triples.append([src_name, rel_type, tgt_name])

        logger.debug(f"Knowledge graph query returned {len(triples)} triples")
        return {"triples": triples}

    except Exception as e:
        logger.error(f"Knowledge graph query error: {e}, {traceback.format_exc()}")
        return f"知识图谱查询失败：{str(e)}"
