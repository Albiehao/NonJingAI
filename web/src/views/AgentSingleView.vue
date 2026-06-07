<template>
  <div class="agent-single-view">
    <!-- 智能体选择弹窗 -->
    <a-modal
      v-model:open="agentModalOpen"
      title="选择智能体"
      :width="800"
      :footer="null"
      :maskClosable="true"
      class="agent-modal"
    >
      <div class="agent-modal-content">
        <div class="agents-grid">
          <div
            v-for="agent in agents"
            :key="agent.id"
            class="agent-card"
            :class="{ selected: agent.id === agentId }"
            @click="selectAgentFromModal(agent.id)"
          >
            <div class="agent-card-header">
              <div class="agent-card-title">
                <span class="agent-card-name">{{ agent.name || 'Unknown' }}</span>
              </div>
              <StarFilled v-if="agent.id === defaultAgentId" class="default-icon" />
              <StarOutlined
                v-else
                @click.prevent="setAsDefaultAgent(agent.id)"
                class="default-icon"
              />
            </div>

            <div class="agent-card-description">
              {{ agent.description || '' }}
            </div>
          </div>
        </div>
      </div>
    </a-modal>

    <!-- 智能体聊天界面 -->
    <AgentChatComponent ref="chatComponentRef" :agent-id="agentId" :single-mode="true">
      <template #header-right>
        <div type="button" class="agent-nav-btn" @click="handleShareChat">
          <Share2 size="18" class="nav-btn-icon" />
          <span class="text">分享</span>
        </div>
      </template>
    </AgentChatComponent>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useRoute, useRouter } from 'vue-router'
import { Share2 } from 'lucide-vue-next'
import { StarFilled, StarOutlined } from '@ant-design/icons-vue'
import AgentChatComponent from '@/components/AgentChatComponent.vue'
import { ChatExporter } from '@/utils/chatExporter'
import { handleChatError } from '@/utils/errorHandler'
import { useAgentStore } from '@/stores/agent'
import { storeToRefs } from 'pinia'

const route = useRoute()
const router = useRouter()
const agentStore = useAgentStore()

const agentId = computed(() => route.params.agent_id)
const chatComponentRef = ref(null)

// 智能体选择弹窗状态
const agentModalOpen = ref(false)

// 从 store 获取智能体数据
const { agents, defaultAgentId } = storeToRefs(agentStore)

// 当前智能体名称
const currentAgentName = computed(() => {
  if (!agentId.value || !agents.value?.length) return '智能体加载中……'
  const agent = agents.value.find((a) => a.id === agentId.value)
  return agent ? agent.name : '未知智能体'
})

// 打开智能体选择弹窗
const openAgentModal = () => {
  agentModalOpen.value = true
}

// 从弹窗中选择智能体 - 切换路由
const selectAgentFromModal = (newAgentId) => {
  if (newAgentId === agentId.value) {
    // 如果选择的是当前智能体，只需要关闭弹窗
    agentModalOpen.value = false
    return
  }

  // 跳转到新的智能体页面
  router.push(`/agent/${newAgentId}`)
  agentModalOpen.value = false
}

// 设置默认智能体
const setAsDefaultAgent = async (agentIdToSet) => {
  try {
    await agentStore.setDefaultAgent(agentIdToSet)
    message.success('已设置为默认智能体')
  } catch (error) {
    handleChatError(error, 'save')
  }
}

const handleShareChat = async () => {
  try {
    const exportData = chatComponentRef.value?.getExportPayload?.()

    if (!exportData) {
      message.warning('当前没有可导出的对话内容')
      return
    }

    const hasMessages = Boolean(exportData.messages?.length)
    const hasOngoingMessages = Boolean(exportData.onGoingMessages?.length)

    if (!hasMessages && !hasOngoingMessages) {
      message.warning('当前对话暂无内容可导出，请先进行对话')
      return
    }

    const result = await ChatExporter.exportToHTML(exportData)
    message.success(`对话已导出为HTML文件: ${result.filename}`)
  } catch (error) {
    if (error?.message?.includes('没有可导出的对话内容')) {
      message.warning('当前对话暂无内容可导出，请先进行对话')
      return
    }
    handleChatError(error, 'export')
  }
}

// 初始化时确保智能体 store 已加载
onMounted(async () => {
  if (!agentStore.isInitialized) {
    try {
      await agentStore.initialize()
    } catch (error) {
      console.error('初始化智能体 store 失败:', error)
    }
  }
})
</script>

<style lang="less" scoped>
.agent-single-view {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: row;
  background: transparent;
}

.user-info-wrapper {
  position: absolute;
  top: 10px;
  right: 20px;
  z-index: 10;
}

// 智能体选择弹窗样式
.agent-modal {
  :deep(.ant-modal-content) {
    border-radius: 8px;
    overflow: hidden;
  }

  :deep(.ant-modal-header) {
    background: var(--gray-0);
    border-bottom: 1px solid var(--gray-200);
    padding: 16px 20px;

    .ant-modal-title {
      font-weight: 600;
      color: var(--gray-900);
    }
  }

  :deep(.ant-modal-body) {
    padding: 20px;
    background: var(--gray-0);
  }

  .agent-modal-content {
    .agents-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 12px;
      max-height: 500px;
      overflow-y: auto;
    }

    .agent-card {
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      padding: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      background: var(--gray-0);

      &:hover {
        border-color: var(--main-color);
      }

      .agent-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;

        .agent-card-title {
          flex: 1;

          .agent-card-name {
            font-size: 16px;
            font-weight: 600;
            color: var(--gray-900);
            line-height: 1.4;
          }
        }

        .default-icon {
          color: var(--color-warning-500);
          font-size: 16px;
          flex-shrink: 0;
          margin-left: 8px;
          cursor: pointer;

          &:hover {
            color: var(--color-warning-600);
          }
        }
      }

      .agent-card-description {
        font-size: 14px;
        color: var(--gray-700);
        line-height: 1.5;
        word-break: break-word;
        white-space: pre-wrap;
      }

      &.selected {
        border-color: var(--main-color);
        background: var(--main-20);

        .agent-card-header .agent-card-title .agent-card-name {
          color: var(--main-color);
        }

        .agent-card-description {
          color: var(--gray-900);
        }
      }
    }
  }
}

// 响应式适配智能体弹窗
@media (max-width: 768px) {
  .agent-modal {
    .agent-modal-content {
      .agents-grid {
        grid-template-columns: 1fr;
      }
    }
  }
}

</style>

<style lang="less">
.agent-nav-btn {
  display: flex;
  gap: 6px;
  padding: 6px 8px;
  justify-content: center;
  align-items: center;
  border-radius: 6px;
  color: var(--gray-900);
  cursor: pointer;
  width: auto;
  font-size: 15px;
  transition: background-color 0.3s;
  border: none;
  background: transparent;

  &:hover {
    background-color: var(--gray-50);
  }

  .nav-btn-icon {
    height: 24px;
  }

  .switch-icon {
    color: var(--gray-500);
    transition: all 0.2s ease;
  }

  &:hover .switch-icon {
    color: var(--main-500);
  }
}
</style>
