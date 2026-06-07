<template>
  <BaseToolCall :tool-call="toolCall" :hide-params="true">
    <template #header>
      <div class="sep-header">
        <span class="note">秘塔搜索</span>
        <span class="separator" v-if="query">|</span>
        <span class="description">{{ query }}</span>
      </div>
    </template>
    <template #result="{ resultContent }">
      <div class="web-search-result">
        <!-- AI 总结模式 -->
        <div class="ai-answer" v-if="parsedData(resultContent).answer">
          <div class="answer-label">AI 总结</div>
          <div class="answer-content">
            {{ parsedData(resultContent).answer }}
          </div>
          <div
            class="references"
            v-if="
              parsedData(resultContent).references &&
              parsedData(resultContent).references.length > 0
            "
          >
            <div class="references-title">参考来源</div>
            <div class="reference-list">
              <div
                v-for="(ref, index) in parsedData(resultContent).references"
                :key="index"
                class="reference-item"
              >
                [{{ ref.id }}]
              </div>
            </div>
          </div>
        </div>

        <!-- 传统网页搜索结果 -->
        <div
          class="search-results"
          v-else-if="
            parsedData(resultContent).results && parsedData(resultContent).results.length > 0
          "
        >
          <div
            v-for="(result, index) in parsedData(resultContent).results"
            :key="index"
            class="search-result-item"
          >
            <div class="result-header">
              <h5 class="result-title">
                <a :href="result.url" target="_blank" rel="noopener noreferrer">
                  {{ result.title }}
                </a>
              </h5>
            </div>

            <div class="result-content">
              {{ result.content || result.snippet }}
            </div>
          </div>
        </div>

        <div v-else-if="parsedData(resultContent).rawText" class="raw-content">
          {{ parsedData(resultContent).rawText }}
        </div>

        <div v-else class="no-results">
          <p>未找到相关搜索结果</p>
        </div>
      </div>
    </template>
  </BaseToolCall>
</template>

<script setup>
import BaseToolCall from '../BaseToolCall.vue'
import { computed } from 'vue'

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
      return { query: '', results: [], response_time: 0, rawText: content }
    }
  }
  return content || { query: '', results: [], response_time: 0 }
}

const parsedData = (content) => parseData(content)

const query = computed(() => {
  const result = parsedData(props.toolCall.tool_call_result?.content)
  if (result?.query) return result.query

  const args = props.toolCall.args || props.toolCall.function?.arguments
  if (!args) return ''
  if (typeof args === 'object') return args.query || args.q || ''
  try {
    const parsed = JSON.parse(args)
    return parsed.query || parsed.q || ''
  } catch (e) {
    return ''
  }
})
</script>

<style lang="less" scoped>
.web-search-result {
  background: var(--gray-0);
  border-radius: 8px;

  .ai-answer {
    padding: 16px;

    .answer-label {
      font-size: 12px;
      font-weight: 600;
      color: var(--main-color);
      margin-bottom: 8px;
      text-transform: uppercase;
    }

    .answer-content {
      font-size: 14px;
      line-height: 1.8;
      color: var(--gray-800);
      white-space: pre-wrap;
    }

    .references {
      margin-top: 16px;
      padding-top: 12px;
      border-top: 1px solid var(--gray-150);

      .references-title {
        font-size: 12px;
        font-weight: 600;
        color: var(--gray-600);
        margin-bottom: 8px;
      }

      .reference-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }

      .reference-item {
        font-size: 11px;
        color: var(--gray-500);
        background: var(--gray-50);
        padding: 2px 8px;
        border-radius: 4px;
      }
    }
  }

  .search-results {
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .search-result-item {
    padding: 12px;
    border-bottom: 1px solid var(--gray-200);
    transition: all 0.2s ease;

    &:last-child {
      border-bottom: none;
    }

    .result-header {
      margin-bottom: 8px;

      .result-title {
        margin: 0;
        font-size: 14px;
        line-height: 1.4;

        a {
          color: var(--main-color);
          text-decoration: none;
          font-weight: 500;

          &:hover {
            color: var(--main-color);
            text-decoration: underline;
          }
        }
      }
    }

    .result-content {
      font-size: 13px;
      line-height: 1.5;
      color: var(--gray-700);
      overflow: hidden;
      display: -webkit-box;
      line-clamp: 3;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
    }
  }

  .raw-content {
    padding: 12px;
    font-size: 13px;
    line-height: 1.5;
    color: var(--gray-700);
    white-space: pre-wrap;
    font-family: monospace;
  }

  .no-results {
    text-align: center;
    color: var(--gray-500);
    padding: 20px;
    font-size: 13px;
  }
}
</style>
