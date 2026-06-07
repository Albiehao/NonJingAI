<template>
  <BaseToolCall :tool-call="toolCall" :hide-params="true">
    <template #header>
      <div class="sep-header">
        <span class="note">知识图谱</span>
        <span class="separator" v-if="query">|</span>
        <span class="description">{{ query }}</span>
      </div>
    </template>
    <template #result="{ resultContent }">
      <div class="knowledge-graph-result">
        <div class="result-summary">找到 {{ totalNodes }} 个节点, {{ totalRelations }} 个关系</div>

        <!-- 图谱可视化容器 -->
        <div
          class="graph-visualization"
          ref="graphContainerRef"
          v-if="totalNodes > 0 || totalRelations > 0"
        >
          <GraphCanvas :graph-data="graphData" ref="graphContainer" style="height: 360px">
            <template #top>
              <div class="graph-controls">
                <a-button
                  @click="refreshGraph"
                  :loading="isRefreshing"
                  title="重新渲染图谱"
                  class="refresh-btn"
                >
                  <ReloadOutlined v-if="!isRefreshing" />
                </a-button>
              </div>
            </template>
          </GraphCanvas>
        </div>
      </div>
    </template>
  </BaseToolCall>
</template>

<script setup>
import { computed, ref, watch, nextTick, onMounted } from 'vue'
import BaseToolCall from '../BaseToolCall.vue'
import { ReloadOutlined } from '@ant-design/icons-vue'
import GraphCanvas from '@/components/GraphCanvas.vue'

const props = defineProps({
  toolCall: {
    type: Object,
    required: true
  }
})

const parseData = (content) => {
  if (typeof content === 'string') {
    try {
      return JSON.parse(content)
    } catch (error) {
      return { triples: [] }
    }
  }
  return content || { triples: [] }
}

const graphContainer = ref(null)
const graphContainerRef = ref(null)
const isRefreshing = ref(false)

const query = computed(() => {
  const args = props.toolCall.args || props.toolCall.function?.arguments
  if (!args) return ''
  let parsedArgs = args
  if (typeof args === 'string') {
    try {
      parsedArgs = JSON.parse(args)
    } catch (e) {
      return ''
    }
  }
  if (typeof parsedArgs === 'object') {
    return parsedArgs.query || parsedArgs.keywords || parsedArgs.q || parsedArgs.entities || ''
  }
  return ''
})

// 计算属性：解析图谱数据
const graphData = computed(() => {
  const data = parseData(props.toolCall.tool_call_result?.content)
  const nodes = new Map()
  const edges = []
  let edgeId = 0

  if (data && typeof data === 'object' && Array.isArray(data.nodes) && Array.isArray(data.edges)) {
    data.nodes.forEach((node) => {
      const id = node.id || node.name || ''
      const name = node.name || node.id || ''
      if (id && !nodes.has(id)) {
        nodes.set(id, { id, name, ...node })
      }
    })
    data.edges.forEach((edge) => {
      const sourceId = edge.source_id || edge.source || ''
      const targetId = edge.target_id || edge.target || ''
      if (sourceId && targetId) {
        edges.push({
          source_id: sourceId,
          target_id: targetId,
          type: edge.type || '',
          id: edge.id || `edge_${edgeId++}`
        })
      }
    })
  } else if (data && typeof data === 'object' && 'triples' in data) {
    const { triples = [] } = data
    triples.forEach((triple) => {
      if (Array.isArray(triple) && triple.length >= 3) {
        const [source, relation, target] = triple
        if (source && typeof source === 'string' && !nodes.has(source)) {
          nodes.set(source, { id: source, name: source })
        }
        if (target && typeof target === 'string' && !nodes.has(target)) {
          nodes.set(target, { id: target, name: target })
        }
        if (source && target && relation && typeof source === 'string' && typeof target === 'string' && typeof relation === 'string') {
          edges.push({
            source_id: source,
            target_id: target,
            type: relation,
            id: `edge_${edgeId++}`
          })
        }
      }
    })
  }

  return {
    nodes: Array.from(nodes.values()),
    edges: edges
  }
})

const totalNodes = computed(() => graphData.value.nodes.length)
const totalRelations = computed(() => graphData.value.edges.length)

// 数据变化时才刷新图表，仅一次
const dataKey = computed(() => {
  const content = props.toolCall.tool_call_result?.content
  return typeof content === 'string' ? content.slice(0, 200) : JSON.stringify(content)
})

watch(dataKey, () => {
  if (graphData.value.nodes.length === 0 && graphData.value.edges.length === 0) return
  nextTick(() => {
    if (graphContainer.value?.refreshGraph) {
      setTimeout(() => graphContainer.value.refreshGraph(), 300)
    }
  })
})

// 组件挂载后刷新一次
onMounted(() => {
  if (graphData.value.nodes.length > 0 || graphData.value.edges.length > 0) {
    nextTick(() => {
      if (graphContainer.value?.refreshGraph) {
        setTimeout(() => graphContainer.value.refreshGraph(), 300)
      }
    })
  }
})

const refreshGraph = () => {
  isRefreshing.value = true
  if (graphContainer.value?.refreshGraph) {
    setTimeout(() => {
      graphContainer.value.refreshGraph()
      setTimeout(() => { isRefreshing.value = false }, 500)
    }, 300)
  } else {
    isRefreshing.value = false
  }
}

defineExpose({ refreshGraph })
</script>

<style lang="less" scoped>
.knowledge-graph-result {
  background: var(--gray-0);
  border-radius: 8px;
  // border: 1px solid var(--gray-200);

  .result-summary {
    padding: 12px 16px;
    background: var(--gray-25);
    font-size: 12px;
    color: var(--gray-600);
    border-bottom: 1px solid var(--gray-100);
  }

  .graph-visualization {
    margin: 8px;
    background: var(--gray-0);
    border-radius: 6px;
    border: 1px solid var(--gray-200);
    min-height: 350px;

    .graph-controls {
      position: absolute;
      top: 8px;
      right: 8px;
      z-index: 1000;

      .refresh-btn {
        width: 24px;
        height: 24px;
        min-width: 24px;
        padding: 0;
        border-radius: 4px;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid var(--gray-300);
        color: var(--gray-600);
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;

        &:hover {
          background: rgba(255, 255, 255, 1);
          border-color: var(--main-color);
          color: var(--main-color);
        }
      }
    }
  }

  .kg-details {
    margin: 8px;
    background: var(--gray-0);
    border-radius: 6px;
    border: 1px solid var(--gray-200);

    :deep(.ant-collapse-header) {
      background: var(--gray-50) !important;
      border-radius: 4px !important;
      margin-bottom: 2px;
      font-size: 13px;
    }

    .entities-list {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding: 6px 0;

      .entity-tag {
        margin: 0;
        cursor: default;
        font-size: 11px;
        padding: 2px 6px;
      }
    }

    .relations-list {
      display: flex;
      flex-direction: column;
      gap: 6px;

      .relation-item {
        padding: 8px 10px;
        background: var(--gray-50);
        border-radius: 4px;
        border-left: 2px solid var(--main-color);

        .relation-content {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 12px;

          .entity-name {
            font-weight: 500;
            color: var(--main-color);
            background: var(--main-50);
            padding: 2px 6px;
            border-radius: 10px;
          }

          .relation-type {
            color: var(--main-color);
            font-weight: 500;
            background: var(--gray-100);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid var(--gray-300);
          }
        }
      }
    }

    .raw-data {
      background: var(--gray-50);
      padding: 10px;
      border-radius: 4px;
      font-size: 11px;
      line-height: 1.4;
      max-height: 200px;
      overflow-y: auto;
      margin: 0;
      color: var(--gray-700);
    }
  }
}
</style>
