<template>
  <div class="chat-container">
    <ChatSidebarComponent
      :current-chat-id="currentChatId"
      :chats-list="chatsList"
      :is-sidebar-open="chatUIStore.isSidebarOpen"
      :is-initial-render="localUIState.isInitialRender"
      :single-mode="props.singleMode"
      :agents="agents"
      :selected-agent-id="currentAgentId"
      :is-creating-new-chat="chatUIStore.creatingNewChat"
      @create-chat="createNewChat"
      @select-chat="selectChat"
      @delete-chat="deleteChat"
      @rename-chat="renameChat"
      @toggle-sidebar="toggleSidebar"
      @open-agent-modal="openAgentModal"
      :class="{
        'sidebar-open': chatUIStore.isSidebarOpen,
        'no-transition': localUIState.isInitialRender
      }"
    />
    <div class="chat">
      <div class="chat-header">
        <div class="header__left">
          <slot name="header-left" class="nav-btn"></slot>
          <div
            type="button"
            class="agent-nav-btn"
            v-if="!chatUIStore.isSidebarOpen"
            @click="toggleSidebar"
          >
            <PanelLeftOpen class="nav-btn-icon" size="18" />
          </div>
          <div
            type="button"
            class="agent-nav-btn"
            v-if="!chatUIStore.isSidebarOpen"
            :class="{ 'is-disabled': chatUIStore.creatingNewChat }"
            @click="createNewChat"
          >
            <LoaderCircle
              v-if="chatUIStore.creatingNewChat"
              class="nav-btn-icon loading-icon"
              size="18"
            />
            <MessageCirclePlus v-else class="nav-btn-icon" size="16" />
            <span class="text">新对话</span>
          </div>
        </div>
        <div class="header__right">
          <!-- AgentState 显示按钮已移动到输入框底部 -->
          <slot name="header-right"></slot>
        </div>
      </div>

      <div class="chat-content-container">
        <div
          class="chat-main"
          ref="chatMainContainer"
          :class="{ 'is-empty': !conversations.length && !isLoadingMessages }"
        >
          <div class="chat-box" ref="messagesContainer">
            <template v-if="conversations.length">
              <div class="conv-box" v-for="(conv, index) in conversations" :key="index">
                <AgentMessageComponent
                  v-for="(message, msgIndex) in conv.messages"
                  :message="message"
                  :key="msgIndex"
                  :is-processing="
                    isProcessing &&
                    conv.status === 'streaming' &&
                    msgIndex === conv.messages.length - 1
                  "
                  :show-refs="showMsgRefs(message)"
                  :agent-id="currentAgentId"
                  @retry="retryMessage(message)"
                />
                <RefsComponent
                  v-if="shouldShowRefs(conv)"
                  :message="getLastMessage(conv)"
                  :show-refs="['model', 'copy']"
                  :is-latest-message="false"
                  :agent-id="currentAgentId"
                />
              </div>
              <div class="generating-status" v-if="isProcessing">
                <div class="generating-indicator">
                  <div class="loading-dots">
                    <div></div>
                    <div></div>
                    <div></div>
                  </div>
                  <span class="generating-text">正在生成回复...</span>
                </div>
              </div>
            </template>

            <div v-else-if="!isLoadingMessages" class="start-view">
              <div class="start-center">
                <!-- Mode Slider -->
                <div class="mode-slider">
                  <button
                    class="mode-option"
                    :class="{ active: startMode === 'ask' }"
                    @click="switchToAskMode"
                  >千寻问农</button>
                  <button
                    class="mode-option"
                    :class="{ active: startMode === 'prescription' }"
                    @click="switchToPrescriptionMode"
                  >千寻有方</button>
                  <div class="slider-bg" :class="{ right: startMode === 'prescription' }"></div>
                </div>

                <!-- Ask Mode -->
                <template v-if="startMode === 'ask'">
                  <h1 class="start-title">{{ currentAgentName }}</h1>
                  <p class="start-subtitle">{{ welcomeDescription }}</p>

                  <div class="start-tags">
                    <span v-for="item in welcomeFeatures" :key="item.label" class="start-tag">
                      <component :is="item.icon" :size="14" />
                      {{ item.label }}
                    </span>
                  </div>

                  <div v-if="exampleQuestions.length" class="start-prompts">
                    <p class="start-prompts-label">
                      <Wheat :size="14" />
                      试试这样问
                    </p>
                    <button
                      v-for="question in exampleQuestions"
                      :key="question.id"
                      type="button"
                      class="start-prompt"
                      @click="handleExampleClick(question.text)"
                    >
                      <span>{{ question.text }}</span>
                      <ArrowRight :size="15" class="start-prompt-arrow" />
                    </button>
                  </div>

                  <p v-if="supportsFileUpload" class="start-note">
                    支持上传作物图片，结合描述获得诊断建议
                  </p>
                </template>

                <!-- Prescription Mode -->
                <template v-if="startMode === 'prescription'">
                  <h1 class="start-title">千寻有方</h1>
                  <p class="start-subtitle">作物病虫害深度调查，并且生成详细报告，精准施策，科学防治</p>

                  <div class="start-tags">
                    <span class="start-tag">
                      <Bug :size="14" />
                      病害诊断
                    </span>
                    <span class="start-tag">
                      <FlaskConical :size="14" />
                      虫害识别
                    </span>
                    <span class="start-tag">
                      <Droplets :size="14" />
                      报告生成
                    </span>
                  </div>

                  <div class="start-prompts">
                    <p class="start-prompts-label">
                      <ScrollText :size="14" />
                      查询处方
                    </p>
                    <button
                      type="button"
                      class="start-prompt"
                      @click="handleExampleClick('水稻稻瘟病怎么防治？')"
                    >
                      <span>水稻稻瘟病怎么防治？</span>
                      <ArrowRight :size="15" class="start-prompt-arrow" />
                    </button>
                    <button
                      type="button"
                      class="start-prompt"
                      @click="handleExampleClick('玉米螟用什么药效果最好？')"
                    >
                      <span>玉米螟用什么药效果最好？</span>
                      <ArrowRight :size="15" class="start-prompt-arrow" />
                    </button>
                    <button
                      type="button"
                      class="start-prompt"
                      @click="handleExampleClick('黄瓜霜霉病的防治方案')"
                    >
                      <span>黄瓜霜霉病的防治方案</span>
                      <ArrowRight :size="15" class="start-prompt-arrow" />
                    </button>
                  </div>
                </template>
              </div>
            </div>
          </div>

          <div class="bottom" :class="{ 'is-start-mode': !conversations.length }">
            <div class="message-input-wrapper">
              <div v-if="isLoadingMessages" class="chat-loading">
                <div class="loading-spinner"></div>
                <span>正在加载消息...</span>
              </div>

              <div class="input-dock">
                <AgentInputArea
                  ref="messageInputRef"
                  v-model="userInput"
                  :is-loading="isProcessing"
                  :disabled="!currentAgent"
                  :send-button-disabled="(!userInput || !currentAgent) && !isProcessing"
                  placeholder="输入问题，或上传作物图片..."
                  :supports-file-upload="supportsFileUpload"
                  :agent-id="currentAgentId"
                  :thread-id="currentChatId"
                  :ensure-thread="ensureActiveThread"
                  :has-state-content="hasAgentStateContent"
                  :is-panel-open="isAgentPanelOpen"
                  :mention="mentionConfig"
                  @send="handleSendOrStop"
                  @attachment-changed="handleAgentStateRefresh"
                  @toggle-panel="toggleAgentPanel"
                />
              </div>

              <div class="bottom-actions" v-if="conversations.length">
                <p class="note">千寻也会犯错，重要农事务必再次咨询专家</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Agent Panel Area -->

        <div
          class="agent-panel-wrapper"
          ref="panelWrapperRef"
          :class="{
            'is-visible': isAgentPanelOpen && hasAgentStateContent,
            'no-transition': isResizing
          }"
          :style="{
            flexBasis: isAgentPanelOpen && hasAgentStateContent ? `${panelRatio * 100}%` : '0px'
          }"
        >
          <AgentPanel
            v-if="isAgentPanelOpen && hasAgentStateContent"
            :agent-state="currentAgentState"
            :thread-id="currentChatId"
            :panel-ratio="panelRatio"
            @refresh="handleAgentStateRefresh"
            @close="toggleAgentPanel"
            @resize="handlePanelResize"
            @resizing="handleResizingChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, nextTick, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import AgentInputArea from '@/components/AgentInputArea.vue'
import AgentMessageComponent from '@/components/AgentMessageComponent.vue'
import ChatSidebarComponent from '@/components/ChatSidebarComponent.vue'
import RefsComponent from '@/components/RefsComponent.vue'
import {
  PanelLeftOpen,
  MessageCirclePlus,
  LoaderCircle,
  ImageIcon,
  BookOpen,
  Sprout,
  ArrowRight,
  Wheat,
  ScrollText,
  Bug,
  FlaskConical,
  Droplets
} from 'lucide-vue-next'
import { handleChatError, handleValidationError } from '@/utils/errorHandler'
import { ScrollController } from '@/utils/scrollController'
import { AgentValidator } from '@/utils/agentValidator'
import { useAgentStore } from '@/stores/agent'
import { useChatUIStore } from '@/stores/chatUI'
import { storeToRefs } from 'pinia'
import { MessageProcessor } from '@/utils/messageProcessor'
import { agentApi, threadApi, databaseApi } from '@/apis'
import { useAgentStreamHandler } from '@/composables/useAgentStreamHandler'
import AgentPanel from '@/components/AgentPanel.vue'

// ==================== PROPS & EMITS ====================
const props = defineProps({
  agentId: { type: String, default: '' },
  singleMode: { type: Boolean, default: true }
})
const emit = defineEmits(['open-config', 'open-agent-modal'])

// ==================== STORE MANAGEMENT ====================
const agentStore = useAgentStore()
const chatUIStore = useChatUIStore()
const {
  agents,
  selectedAgentId,
  defaultAgentId,
  selectedAgentConfigId,
  agentConfig,
  configurableItems
} = storeToRefs(agentStore)

// ==================== LOCAL CHAT & UI STATE ====================
const userInput = ref('')

// 从智能体元数据获取示例问题
const exampleQuestions = computed(() => {
  const agentId = currentAgentId.value
  let examples = []
  if (agentId && agents.value && agents.value.length > 0) {
    const agent = agents.value.find((a) => a.id === agentId)
    examples = agent ? agent.examples || [] : []
  }
  return examples.map((text, index) => ({
    id: index + 1,
    text: text
  }))
})

// Keep per-thread streaming scratch data in a consistent shape.
const createOnGoingConvState = () => ({
  msgChunks: {},
  currentRequestKey: null,
  currentAssistantKey: null,
  toolCallBuffers: {}
})

// 业务状态（保留在组件本地）
const chatState = reactive({
  currentThreadId: null,
  // 以threadId为键的线程状态
  threadStates: {}
})

// 组件级别的线程和消息状态
const threads = ref([])
const threadMessages = ref({})

// 本地 UI 状态（仅在本组件使用）
const localUIState = reactive({
  isInitialRender: true
})

const router = useRouter()

// Start view mode toggle - computed from current agent
const startMode = computed(() => currentAgentId.value === 'CropAgent' ? 'prescription' : 'ask')
const switchToAskMode = () => {
  if (startMode.value === 'prescription') {
    const id = defaultAgentId.value || agents.value[0]?.id
    if (id && id !== currentAgentId.value) {
      if (props.singleMode) {
        router.push(`/agent/${id}`)
      } else {
        agentStore.selectAgent(id)
      }
    }
  }
}
const switchToPrescriptionMode = () => {
  if (startMode.value !== 'prescription') {
    if (props.singleMode) {
      router.push('/agent/CropAgent')
    } else {
      agentStore.selectAgent('CropAgent')
    }
  }
}

// Mention resources
const availableKnowledgeBases = ref([])

// Agent Panel State
const isAgentPanelOpen = ref(false)
const isResizing = ref(false)
const panelRatio = ref(0.4) // 面板宽度比例 (0-1)
const panelWrapperRef = ref(null) // 直接操作 DOM
const minPanelRatio = 0.3 // 最小比例 30%
const maxPanelRatio = 0.6 // 最大比例 60%
let panelContainerWidth = 0

// ==================== COMPUTED PROPERTIES ====================
const currentAgentId = computed(() => {
  if (props.singleMode) {
    return props.agentId || defaultAgentId.value
  } else {
    return selectedAgentId.value
  }
})

const currentAgentName = computed(() => {
  const agent = currentAgent.value
  return agent ? agent.name : '智能体'
})

const welcomeDescription = computed(() => {
  const desc = currentAgent.value?.description
  if (desc) return desc
  return '面向种植、巡田和农技服务，支持作物图片识别、病虫害诊断与自然语言问答。'
})

const welcomeFeatures = [
  { label: '图像识别', desc: '上传叶片或果实照片', icon: ImageIcon },
  { label: '农技问答', desc: '追问原因与处置建议', icon: BookOpen },
  { label: '田间诊断', desc: '结合现场描述分析', icon: Sprout }
]

const currentAgent = computed(() => {
  if (!currentAgentId.value || !agents.value || !agents.value.length) return null
  return agents.value.find((a) => a.id === currentAgentId.value) || null
})
const chatsList = computed(() => threads.value || [])
const currentChatId = computed(() => chatState.currentThreadId)
const currentThread = computed(() => {
  if (!currentChatId.value) return null
  return threads.value.find((thread) => thread.id === currentChatId.value) || null
})

// 检查当前智能体是否支持文件上传
const supportsFileUpload = computed(() => {
  if (!currentAgent.value) return false
  const capabilities = currentAgent.value.capabilities || []
  return capabilities.includes('file_upload')
})
const supportsTodo = computed(() => {
  if (!currentAgent.value) return false
  const capabilities = currentAgent.value.capabilities || []
  return capabilities.includes('todo')
})

const supportsFiles = computed(() => {
  if (!currentAgent.value) return false
  const capabilities = currentAgent.value.capabilities || []
  return capabilities.includes('files')
})

// AgentState 相关计算属性
const currentAgentState = computed(() => {
  return currentChatId.value ? getThreadState(currentChatId.value)?.agentState || null : null
})

const countFiles = (files) => {
  // 支持 dict 格式（StateBackend 格式）和 array 格式
  if (!files) return 0
  if (typeof files === 'object' && !Array.isArray(files)) {
    // dict 格式: {"/attachments/file.md": {...}, ...}
    return Object.keys(files).length
  }
  if (Array.isArray(files)) {
    // array 格式
    let c = 0
    for (const item of files) {
      if (item && typeof item === 'object') c += Object.keys(item).length
    }
    return c
  }
  return 0
}

const hasAgentStateContent = computed(() => {
  const s = currentAgentState.value
  if (!s) return false
  const todoCount = Array.isArray(s.todos) ? s.todos.length : 0
  const fileCount = countFiles(s.files)
  return todoCount > 0 || fileCount > 0
})

const mentionConfig = computed(() => {
  const rawFiles = currentAgentState.value?.files || {}
  const files = []

  // 处理 files - 兼容字典格式 {"/path/file": {content: [...]}} 和旧数组格式
  if (typeof rawFiles === 'object' && !Array.isArray(rawFiles) && rawFiles !== null) {
    // 新格式：字典格式 {"/attachments/xxx/file.md": {...}}
    Object.entries(rawFiles).forEach(([filePath, fileData]) => {
      files.push({
        path: filePath,
        ...fileData
      })
    })
  } else if (Array.isArray(rawFiles)) {
    // 旧格式：数组格式
    rawFiles.forEach((item) => {
      if (typeof item === 'object' && item !== null) {
        Object.entries(item).forEach(([filePath, fileData]) => {
          files.push({
            path: filePath,
            ...fileData
          })
        })
      }
    })
  }

  // Filter KBs based on agent config
  const configItems = configurableItems.value || {}
  const currentConfig = agentConfig.value || {}
  const allowedKbNames = new Set()

  Object.entries(configItems).forEach(([key, item]) => {
    const kind = item?.template_metadata?.kind
    const val = currentConfig[key]

    if (Array.isArray(val)) {
      if (kind === 'knowledges') {
        val.forEach((v) => allowedKbNames.add(v))
      }
    }
  })

  const knowledgeBases = availableKnowledgeBases.value.filter((kb) => allowedKbNames.has(kb.name))

  if (!files.length && !knowledgeBases.length) return null

  return {
    files,
    knowledgeBases,
  }
})

const currentThreadMessages = computed(() => threadMessages.value[currentChatId.value] || [])

// 计算是否显示Refs组件的条件
const shouldShowRefs = computed(() => {
  return (conv) => {
    return (
      getLastMessage(conv) &&
      conv.status !== 'streaming'
    )
  }
})

// 当前线程状态的computed属性
const currentThreadState = computed(() => {
  return getThreadState(currentChatId.value)
})

const onGoingConvMessages = computed(() => {
  const threadState = currentThreadState.value
  if (!threadState || !threadState.onGoingConv) return []

  const msgs = Object.values(threadState.onGoingConv.msgChunks).map(
    MessageProcessor.mergeMessageChunk
  )
  return msgs.length > 0
    ? MessageProcessor.convertToolResultToMessages(msgs).filter((msg) => msg.type !== 'tool')
    : []
})

const historyConversations = computed(() => {
  return MessageProcessor.convertServerHistoryToMessages(currentThreadMessages.value)
})

const conversations = computed(() => {
  const historyConvs = historyConversations.value

  // 如果有进行中的消息且线程状态显示正在流式处理，添加进行中的对话
  if (onGoingConvMessages.value.length > 0) {
    const onGoingConv = {
      messages: onGoingConvMessages.value,
      status: 'streaming'
    }
    return [...historyConvs, onGoingConv]
  }
  return historyConvs
})

const isLoadingMessages = computed(() => chatUIStore.isLoadingMessages)
const isStreaming = computed(() => {
  const threadState = currentThreadState.value
  return threadState ? threadState.isStreaming : false
})
const isProcessing = computed(() => isStreaming.value)

// ==================== SCROLL & RESIZE HANDLING ====================
const scrollController = new ScrollController('.chat-box')

onMounted(() => {
  nextTick(() => {
    const chatBoxContainer = document.querySelector('.chat-box')
    if (chatBoxContainer) {
      chatBoxContainer.addEventListener('scroll', scrollController.handleScroll, { passive: true })
    }
  })
  setTimeout(() => {
    localUIState.isInitialRender = false
  }, 300)
})

onUnmounted(() => {
  scrollController.cleanup()
  // 清理所有线程状态
  resetOnGoingConv()
})

// ==================== THREAD STATE MANAGEMENT ====================
// 获取指定线程的状态，如果不存在则创建
const getThreadState = (threadId) => {
  if (!threadId) return null
  if (!chatState.threadStates[threadId]) {
    chatState.threadStates[threadId] = {
      isStreaming: false,
      streamAbortController: null,
      onGoingConv: createOnGoingConvState(),
      agentState: null // 添加 agentState 字段
    }
  }
  return chatState.threadStates[threadId]
}

// 清理指定线程的状态
const cleanupThreadState = (threadId) => {
  if (!threadId) return
  const threadState = chatState.threadStates[threadId]
  if (threadState) {
    if (threadState.streamAbortController) {
      threadState.streamAbortController.abort()
    }
    delete chatState.threadStates[threadId]
  }
}

// ==================== STREAM HANDLING LOGIC ====================
const resetOnGoingConv = (threadId = null) => {
  console.log(
    `🔄 [RESET] Resetting on going conversation: ${new Date().toLocaleTimeString()}.${new Date().getMilliseconds()}`,
    threadId
  )

  const targetThreadId = threadId || currentChatId.value

  if (targetThreadId) {
    // 清理指定线程的状态
    const threadState = getThreadState(targetThreadId)
    if (threadState) {
      if (threadState.streamAbortController) {
        threadState.streamAbortController.abort()
        threadState.streamAbortController = null
      }

      // 直接重置对话状态
      threadState.onGoingConv = createOnGoingConvState()
    }
  } else {
    // 如果没有当前线程，清理所有线程状态
    Object.keys(chatState.threadStates).forEach((tid) => {
      cleanupThreadState(tid)
    })
  }
}

// ==================== 线程管理方法 ====================
// 获取当前智能体的线程列表
const fetchThreads = async () => {
  const agentList = agents.value
  if (!agentList || !agentList.length) return

  chatUIStore.isLoadingThreads = true
  try {
    const allThreads = []
    for (const agent of agentList) {
      const fetchedThreads = await threadApi.getThreads(agent.id)
      if (fetchedThreads && fetchedThreads.length) {
        allThreads.push(...fetchedThreads.map((t) => ({ ...t, agent_id: t.agent_id || agent.id })))
      }
    }
    // Sort by creation date, newest first
    allThreads.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    threads.value = allThreads
  } catch (error) {
    console.error('Failed to fetch threads:', error)
    handleChatError(error, 'fetch')
    throw error
  } finally {
    chatUIStore.isLoadingThreads = false
  }
}

// 创建新线程
const createThread = async (agentId, title = '新的对话') => {
  if (!agentId) return null

  chatState.isCreatingThread = true
  try {
    const thread = await threadApi.createThread(agentId, title)
    if (thread) {
      threads.value.unshift(thread)
      threadMessages.value[thread.id] = []
    }
    return thread
  } catch (error) {
    console.error('Failed to create thread:', error)
    handleChatError(error, 'create')
    throw error
  } finally {
    chatState.isCreatingThread = false
  }
}

// 删除线程
const deleteThread = async (threadId) => {
  if (!threadId) return

  chatState.isDeletingThread = true
  try {
    await threadApi.deleteThread(threadId)
    threads.value = threads.value.filter((thread) => thread.id !== threadId)
    delete threadMessages.value[threadId]

    if (chatState.currentThreadId === threadId) {
      chatState.currentThreadId = null
    }
  } catch (error) {
    console.error('Failed to delete thread:', error)
    handleChatError(error, 'delete')
    throw error
  } finally {
    chatState.isDeletingThread = false
  }
}

// 更新线程标题
const updateThread = async (threadId, title) => {
  if (!threadId || !title) return

  const normalizedTitle = String(title).replace(/\s+/g, ' ').trim().slice(0, 255)
  if (!normalizedTitle) return

  chatState.isRenamingThread = true
  try {
    await threadApi.updateThread(threadId, normalizedTitle)
    const thread = threads.value.find((t) => t.id === threadId)
    if (thread) {
      thread.title = normalizedTitle
    }
  } catch (error) {
    console.error('Failed to update thread:', error)
    handleChatError(error, 'update')
    throw error
  } finally {
    chatState.isRenamingThread = false
  }
}

// 获取线程消息
const fetchThreadMessages = async ({ agentId, threadId, delay = 0 }) => {
  if (!threadId || !agentId) return

  // 如果指定了延迟，等待指定时间（用于确保后端数据库事务提交）
  if (delay > 0) {
    await new Promise((resolve) => setTimeout(resolve, delay))
  }

  try {
    const response = await agentApi.getAgentHistory(agentId, threadId)
    console.log(
      `🔄 [FETCH] Thread messages: ${new Date().toLocaleTimeString()}.${new Date().getMilliseconds()}`,
      response
    )
    threadMessages.value[threadId] = response.history || []
  } catch (error) {
    handleChatError(error, 'load')
    throw error
  }
}

const fetchAgentState = async (agentId, threadId) => {
  if (!agentId || !threadId) return
  try {
    const res = await agentApi.getAgentState(agentId, threadId)
    // 确保更新 currentChatId 对应的 state，因为 currentAgentState 依赖它
    // 如果 currentChatId 为 null，使用传入的 threadId
    const targetChatId = currentChatId.value || threadId
    console.log(
      '[fetchAgentState] agentId:',
      agentId,
      'threadId:',
      threadId,
      'targetChatId:',
      targetChatId,
      'agent_state:',
      JSON.stringify(res.agent_state || {})?.slice(0, 200)
    )
    const ts = getThreadState(targetChatId)
    if (ts) {
      ts.agentState = res.agent_state || null
    } else {
      // 如果 targetChatId 对应的 state 不存在，创建一个
      const newTs = getThreadState(threadId)
      if (newTs) newTs.agentState = res.agent_state || null
    }
  } catch (error) {}
}

const fetchMentionResources = async () => {
  try {
    const dbsRes = await databaseApi.getAccessibleDatabases().catch(() => ({ databases: [] }))
    availableKnowledgeBases.value = dbsRes.databases || []
  } catch (e) {
    console.warn('Failed to fetch mention resources', e)
  }
}

const ensureActiveThread = async (title = '新的对话') => {
  if (currentChatId.value) return currentChatId.value
  try {
    const newThread = await createThread(currentAgentId.value, title || '新的对话')
    if (newThread) {
      chatState.currentThreadId = newThread.id
      return newThread.id
    }
  } catch (error) {
    // createThread 已处理错误提示
  }
  return null
}

const { handleAgentResponse } = useAgentStreamHandler({
  getThreadState,
  currentAgentId,
  supportsTodo,
  supportsFiles
})

// 发送消息并处理流式响应
const sendMessage = async ({
  agentId,
  threadId,
  text,
  signal = undefined,
  imageData = undefined
}) => {
  if (!agentId || !threadId || !text) {
    const error = new Error('Missing agent, thread, or message text')
    handleChatError(error, 'send')
    return Promise.reject(error)
  }

  // 如果是新对话，用消息内容作为标题
  if ((threadMessages.value[threadId] || []).length === 0) {
    const autoTitle = text.replace(/\s+/g, ' ').trim().slice(0, 255)
    if (autoTitle) {
      void updateThread(threadId, autoTitle).catch(() => {})
    }
  }

  const requestData = {
    query: text,
    config: {
      thread_id: threadId,
      ...(selectedAgentConfigId.value ? { agent_config_id: selectedAgentConfigId.value } : {})
    }
  }

  // 如果有图片，添加到请求中
  if (imageData && imageData.imageUrl) {
    requestData.image_url = imageData.imageUrl
  }

  try {
    return await agentApi.sendAgentMessage(agentId, requestData, signal ? { signal } : undefined)
  } catch (error) {
    handleChatError(error, 'send')
    throw error
  }
}

// ==================== CHAT ACTIONS ====================
// 检查第一个对话是否为空
const isFirstChatEmpty = () => {
  if (threads.value.length === 0) return false
  const firstThread = threads.value[0]
  const firstThreadMessages = threadMessages.value[firstThread.id] || []
  return firstThreadMessages.length === 0
}

// 如果第一个对话为空，直接切换到第一个对话
const switchToFirstChatIfEmpty = async () => {
  if (threads.value.length > 0 && isFirstChatEmpty()) {
    await selectChat(threads.value[0].id)
    return true
  }
  return false
}

const createNewChat = async () => {
  if (
    !AgentValidator.validateAgentId(currentAgentId.value, '创建对话') ||
    chatUIStore.creatingNewChat
  )
    return

  // 如果第一个对话为空，直接切换到第一个对话而不是创建新对话
  if (await switchToFirstChatIfEmpty()) return

  // 只有当当前对话是第一个对话且为空时，才阻止创建新对话
  const currentThreadIndex = threads.value.findIndex((thread) => thread.id === currentChatId.value)
  if (currentChatId.value && conversations.value.length === 0 && currentThreadIndex === 0) return

  chatUIStore.creatingNewChat = true
  try {
    const newThread = await createThread(currentAgentId.value, '新的对话')
    if (newThread) {
      // 中断之前线程的流式输出（如果存在）
      const previousThreadId = chatState.currentThreadId
      if (previousThreadId) {
        const previousThreadState = getThreadState(previousThreadId)
        if (previousThreadState?.isStreaming && previousThreadState.streamAbortController) {
          previousThreadState.streamAbortController.abort()
          previousThreadState.isStreaming = false
          previousThreadState.streamAbortController = null
        }
      }

      chatState.currentThreadId = newThread.id
    }
  } catch (error) {
    handleChatError(error, 'create')
  } finally {
    chatUIStore.creatingNewChat = false
  }
}

const selectChat = async (chatId) => {
  const thread = threads.value.find((t) => t.id === chatId)
  if (!thread) return
  const threadAgentId = thread.agent_id

  if (
    !AgentValidator.validateAgentIdWithError(
      threadAgentId,
      '选择对话',
      handleValidationError
    )
  )
    return

  // 中断之前线程的流式输出（如果存在）
  const previousThreadId = chatState.currentThreadId
  if (previousThreadId && previousThreadId !== chatId) {
    const previousThreadState = getThreadState(previousThreadId)
    if (previousThreadState?.isStreaming && previousThreadState.streamAbortController) {
      previousThreadState.streamAbortController.abort()
      previousThreadState.isStreaming = false
      previousThreadState.streamAbortController = null
    }
  }

  chatState.currentThreadId = chatId
  chatUIStore.isLoadingMessages = true
  try {
    await fetchThreadMessages({ agentId: threadAgentId, threadId: chatId })
  } catch (error) {
    handleChatError(error, 'load')
  } finally {
    chatUIStore.isLoadingMessages = false
  }

  await nextTick()
  scrollController.scrollToBottomStaticForce()
  await fetchAgentState(threadAgentId, chatId)
}

const deleteChat = async (chatId) => {
  const thread = threads.value.find((t) => t.id === chatId)
  if (!thread) return
  const threadAgentId = thread.agent_id

  if (
    !AgentValidator.validateAgentIdWithError(
      threadAgentId,
      '删除对话',
      handleValidationError
    )
  )

    return
  try {
    await deleteThread(chatId)
    if (chatState.currentThreadId === chatId) {
      chatState.currentThreadId = null
      // 如果删除的是当前对话，自动创建新对话
      await createNewChat()
    } else if (chatsList.value.length > 0) {
      // 如果删除的不是当前对话，选择第一个可用对话
      await selectChat(chatsList.value[0].id)
    }
  } catch (error) {
    handleChatError(error, 'delete')
  }
}

const renameChat = async (data) => {
  let { chatId, title } = data
  if (
    !AgentValidator.validateRenameOperation(
      chatId,
      title,
      currentAgentId.value,
      handleValidationError
    )
  )
    return
  if (title.length > 30) title = title.slice(0, 30)
  try {
    await updateThread(chatId, title)
  } catch (error) {
    handleChatError(error, 'rename')
  }
}

const handleSendMessage = async ({ image } = {}) => {
  console.log('AgentChatComponent: handleSendMessage payload image:', image)
  const text = userInput.value.trim()
  if ((!text && !image) || !currentAgent.value || isProcessing.value) return

  let threadId = currentChatId.value
  if (!threadId) {
    threadId = await ensureActiveThread(text)
    if (!threadId) {
      message.error('创建对话失败，请重试')
      return
    }
  }

  userInput.value = ''

  await nextTick()
  scrollController.scrollToBottom(true)

  const threadState = getThreadState(threadId)
  if (!threadState) return

  threadState.isStreaming = true
  resetOnGoingConv(threadId)
  threadState.streamAbortController = new AbortController()

  try {
    const response = await sendMessage({
      agentId: currentAgentId.value,
      threadId: threadId,
      text: text,
      signal: threadState.streamAbortController?.signal,
      imageData: image
    })

    await handleAgentResponse(response, threadId)
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error('Stream error:', error)
      handleChatError(error, 'send')
    } else {
      console.warn('[Interrupted] Catch')
    }
    threadState.isStreaming = false
  } finally {
    threadState.streamAbortController = null
    // 异步加载历史记录，保持当前消息显示直到历史记录加载完成
    fetchThreadMessages({ agentId: currentAgentId.value, threadId: threadId }).finally(() => {
      // 历史记录加载完成后，安全地清空当前进行中的对话
      resetOnGoingConv(threadId)
      scrollController.scrollToBottom()
    })
  }
}

// 发送或中断
const handleSendOrStop = async (payload) => {
  const threadId = currentChatId.value
  const threadState = getThreadState(threadId)
  if (isProcessing.value && threadState && threadState.streamAbortController) {
    // 中断生成
    threadState.streamAbortController.abort()

    // 中断后刷新消息历史，确保显示最新的状态
    try {
      await fetchThreadMessages({ agentId: currentAgentId.value, threadId: threadId })
      message.info('已中断对话生成')
    } catch (error) {
      console.error('刷新消息历史失败:', error)
      message.info('已中断对话生成')
    }
    return
  }
  await handleSendMessage(payload)
}

// 处理示例问题点击
const handleExampleClick = (questionText) => {
  userInput.value = questionText
  nextTick(() => {
    handleSendMessage()
  })
}

const buildExportPayload = () => {
  const agentId = currentAgentId.value
  let agentDescription = ''
  if (agentId && agents.value && agents.value.length > 0) {
    const agent = agents.value.find((a) => a.id === agentId)
    agentDescription = agent ? agent.description || '' : ''
  }

  const payload = {
    chatTitle: currentThread.value?.title || '新对话',
    agentName: currentAgentName.value || currentAgent.value?.name || '智能助手',
    agentDescription: agentDescription || currentAgent.value?.description || '',
    messages: conversations.value ? JSON.parse(JSON.stringify(conversations.value)) : [],
    onGoingMessages: onGoingConvMessages.value
      ? JSON.parse(JSON.stringify(onGoingConvMessages.value))
      : []
  }

  return payload
}

defineExpose({
  getExportPayload: buildExportPayload
})

const toggleSidebar = () => {
  chatUIStore.toggleSidebar()
}
const openAgentModal = () => emit('open-agent-modal')

const handleAgentStateRefresh = async (threadId = null) => {
  if (!currentAgentId.value) return
  // 优先使用传入的 threadId，否则使用当前的 currentChatId
  let chatId = threadId || currentChatId.value
  console.log(
    '[handleAgentStateRefresh] input threadId:',
    threadId,
    'currentChatId:',
    currentChatId.value,
    'final chatId:',
    chatId
  )
  if (!chatId) return
  await fetchAgentState(currentAgentId.value, chatId)
}

const toggleAgentPanel = () => {
  isAgentPanelOpen.value = !isAgentPanelOpen.value
}

// 处理面板宽度调整（使用比例）
// 向右拖动(deltaX > 0)让面板变窄，向左拖动(deltaX < 0)让面板变宽
const handlePanelResize = (deltaX) => {
  if (!panelWrapperRef.value) return

  // 初始化容器宽度
  if (!panelContainerWidth) {
    const container = document.querySelector('.chat-content-container')
    panelContainerWidth = container ? container.clientWidth : window.innerWidth
  }

  const currentWidth = panelWrapperRef.value.offsetWidth
  // 反转 deltaX：向右拖(deltaX > 0)让面板变窄
  const newWidth = currentWidth - deltaX
  const newRatio = newWidth / panelContainerWidth

  // 限制在合理范围内
  if (newRatio >= minPanelRatio && newRatio <= maxPanelRatio) {
    // 直接操作 DOM，不触发 Vue 响应式，使用 !important 确保不被覆盖
    panelWrapperRef.value.style.setProperty('flex', `0 0 ${newWidth}px`, 'important')
  }
}

// 拖拽状态变化时，同步最终状态到 Vue 响应式数据
const handleResizingChange = (isResizingState) => {
  isResizing.value = isResizingState

  // 拖拽结束时，同步 DOM 宽度到响应式数据
  if (!isResizingState && panelWrapperRef.value && panelContainerWidth) {
    const finalWidth = panelWrapperRef.value.offsetWidth
    panelRatio.value = finalWidth / panelContainerWidth
    panelContainerWidth = 0 // 重置，供下次使用
  }
}

// ==================== HELPER FUNCTIONS ====================
const getLastMessage = (conv) => {
  if (!conv?.messages?.length) return null
  for (let i = conv.messages.length - 1; i >= 0; i--) {
    if (conv.messages[i].type === 'ai') return conv.messages[i]
  }
  return null
}

const showMsgRefs = (msg) => {
  if (msg.isLast && msg.status === 'finished') {
    return ['copy']
  }
  return false
}

// ==================== LIFECYCLE & WATCHERS ====================
const loadChatsList = async () => {
  if (!agents.value || !agents.value.length) {
    console.warn('No agents available, cannot load chats list')
    threads.value = []
    chatState.currentThreadId = null
    return
  }

  try {
    await fetchThreads()

    // 如果当前线程不在线程列表中，清空当前线程
    if (
      chatState.currentThreadId &&
      !threads.value.find((t) => t.id === chatState.currentThreadId)
    ) {
      chatState.currentThreadId = null
    }

    // 如果有线程但没有选中任何线程，自动选择第一个
    if (threads.value.length > 0 && !chatState.currentThreadId) {
      await selectChat(threads.value[0].id)
    }
  } catch (error) {
    handleChatError(error, 'load')
  }
}

const initAll = async () => {
  try {
    if (!agentStore.isInitialized) {
      await agentStore.initialize()
    }
    await fetchMentionResources()
  } catch (error) {
    handleChatError(error, 'load')
  }
}

onMounted(async () => {
  await initAll()
  scrollController.enableAutoScroll()
})

watch(
  currentAgentId,
  async (newAgentId) => {
    if (newAgentId) {
      // 等待 agents 加载完成后再获取线程列表
      if (agents.value && agents.value.length) {
        await loadChatsList()
      } else {
        // agents 还未加载，通过 watcher 等待
        const unwatch = watch(agents, async (val) => {
          if (val && val.length) {
            unwatch()
            await loadChatsList()
          }
        }, { immediate: false })
      }
    } else {
      threads.value = []
      chatState.currentThreadId = null
      threadMessages.value = {}
      resetOnGoingConv()
    }
  },
  { immediate: true }
)

watch(
  conversations,
  () => {
    scrollController.scrollToBottom()
  },
  { deep: true, flush: 'post' }
)
</script>

<style lang="less" scoped>
@import '@/assets/css/main.css';
@import '@/assets/css/animations.less';

.chat-container {
  display: flex;
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  background: linear-gradient(rgba(255, 255, 255, 0.65), rgba(255, 255, 255, 0.95)), url('/zj-bj.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

  > * {
    position: relative;
    z-index: 1;
  }
}

.chat {
  position: relative;
  isolation: isolate;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
  transition: all 0.3s ease;
  background: transparent;

  .chat-header {
    user-select: none;
    z-index: 2;
    height: var(--header-height);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 16px;
    flex-shrink: 0;
    background: transparent;
    border-bottom: none;

    .header__left,
    .header__right {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .switch-icon {
      color: var(--gray-500);
      transition: color 0.2s ease;
    }

    .agent-nav-btn:hover .switch-icon {
      color: var(--main-500);
    }
  }
}

.chat-content-container {
  flex: 1;
  display: flex;
  flex-direction: row;
  overflow: hidden;
  position: relative;
  z-index: 1;
  width: 100%;
  contain: layout;
}

.chat-main {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  z-index: 1;
  transition:
    flex-basis 0.3s cubic-bezier(0.4, 0, 0.2, 1),
    width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 0;
  background: transparent;
}

.chat-main.is-empty .chat-box {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-top: min(16vh, 110px);
}

.agent-panel-wrapper {
  flex: 0 0 auto;
  height: calc(100% - 56px);
  overflow: hidden;
  z-index: 20;
  margin: 28px 8px;
  margin-left: 0;
  background: var(--gray-0);
  border-radius: 12px;
  box-shadow: 0 4px 20px var(--shadow-1);
  border: 1px solid var(--gray-150);
  min-width: 0;
  will-change: flex-basis;
}

/* Workbench transition animations */
.agent-panel-wrapper {
  transition: flex-basis 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  transform: translateX(10px);
  margin-left: -16px;
}

.agent-panel-wrapper.is-visible {
  opacity: 1;
  transform: translateX(0);
  margin-left: 0;
}

.agent-panel-wrapper.no-transition {
  transition: none !important;
}

/* Mode Slider */
.mode-slider {
  position: relative;
  display: inline-flex;
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 999px;
  padding: 4px;
  margin-bottom: 40px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);

  .mode-option {
    position: relative;
    z-index: 2;
    padding: 10px 32px;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--gray-600);
    background: transparent;
    border: none;
    border-radius: 999px;
    cursor: pointer;
    transition: color 0.25s ease;
    white-space: nowrap;

    &.active {
      color: var(--gray-0);
    }
  }

  .slider-bg {
    position: absolute;
    z-index: 1;
    top: 4px;
    left: 4px;
    width: calc(50% - 4px);
    height: calc(100% - 8px);
    background: var(--main-700);
    border-radius: 999px;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 8px rgba(4, 106, 130, 0.25);

    &.right {
      transform: translateX(100%);
    }
  }
}

.start-view {
  width: 100%;
  flex: 1;
  display: flex;
  justify-content: center;
  padding: 0 3rem 2.5rem;
}

.start-center {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 720px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.start-title {
  margin: 16px 0 12px;
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.3;
  color: var(--gray-1000);
}

.start-subtitle {
  margin: 0 auto 32px;
  max-width: 560px;
  font-size: 1rem;
  line-height: 1.75;
  color: var(--gray-600);
}

.start-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-bottom: 40px;
}

.start-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--main-800);
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(57, 150, 174, 0.15);
  border-radius: 999px;
  backdrop-filter: blur(6px);

  svg {
    color: var(--main-600);
  }
}

.start-prompts {
  text-align: left;
  margin-bottom: 20px;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 24px rgba(90, 130, 100, 0.06);
}

.start-prompts-label {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 14px;
  padding: 0;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--main-700);
  text-transform: none;

  svg {
    color: var(--main-600);
  }
}

.start-prompt {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
  margin-bottom: 6px;
  padding: 12px 12px;
  text-align: left;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--gray-800);
  background: rgba(255, 255, 255, 0.5);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition:
    background 0.15s ease,
    color 0.15s ease;

  span {
    flex: 1;
    min-width: 0;
  }

  &:hover {
    background: rgba(255, 255, 255, 0.92);
    color: var(--main-800);

    .start-prompt-arrow {
      opacity: 1;
      transform: translateX(2px);
    }
  }
}

.start-prompt-arrow {
  flex-shrink: 0;
  color: var(--main-600);
  opacity: 0.45;
  transition:
    opacity 0.15s ease,
    transform 0.15s ease;
}

.start-note {
  margin: 8px 0 0;
  font-size: 0.75rem;
  color: var(--gray-500);
}

.chat-loading {
  padding: 0 50px;
  text-align: center;
  position: absolute;
  top: 20%;
  width: 100%;
  z-index: 9;
  animation: slideInUp 0.5s ease-out;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;

  span {
    color: var(--gray-700);
    font-size: 14px;
  }

  .loading-spinner {
    width: 20px;
    height: 20px;
    border: 2px solid var(--gray-200);
    border-top-color: var(--main-color);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
}

.chat-box {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  flex: 1 1 auto;
  min-height: 0;
  padding: 0 2.5rem 1rem;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  scrollbar-width: thin;
}

.conv-box {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 1rem 0 1.5rem;
  margin-bottom: 0.75rem;
  background: transparent;
  border: none;
  border-radius: 0;
}

.bottom {
  flex-shrink: 0;
  width: 100%;
  padding: 0 2.5rem 24px;
  background: linear-gradient(180deg, transparent 0%, #f8faf7 40%);
  z-index: 2;

  .message-input-wrapper {
    width: 100%;
    max-width: 900px;
    margin: 0 auto;

    .bottom-actions {
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .note {
      font-size: 12px;
      color: var(--gray-500);
      margin: 6px 0 0;
      user-select: none;
      text-align: center;
    }
  }

  &.is-start-mode {
    padding-top: 12px;
  }
}

.input-dock {
  width: 100%;

  :deep(.input-box) {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);

    &:focus-within {
      border-color: var(--main-300);
      box-shadow: 0 6px 28px rgba(4, 106, 130, 0.12);
    }
  }
}

.loading-dots {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
}

.loading-dots div {
  width: 6px;
  height: 6px;
  background: linear-gradient(135deg, var(--main-color), var(--main-700));
  border-radius: 50%;
  animation: dotPulse 1.4s infinite ease-in-out both;
}

.loading-dots div:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots div:nth-child(2) {
  animation-delay: -0.16s;
}

.loading-dots div:nth-child(3) {
  animation-delay: 0s;
}

.generating-status {
  display: flex;
  justify-content: flex-start;
  padding: 0.5rem 0 1rem;
  animation: fadeInUp 0.4s ease-out;
}

.generating-indicator {
  display: flex;
  align-items: center;
  padding: 0.65rem 1rem;
  background: var(--gray-0);
  border: 1px solid var(--gray-100);
  border-radius: 12px;

  .generating-text {
    margin-left: 12px;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.025em;
    /* 恢复灰色调：深灰 -> 亮灰(高光) -> 深灰 */
    background: linear-gradient(
      90deg,
      var(--gray-700) 0%,
      var(--gray-700) 40%,
      var(--gray-300) 45%,
      var(--gray-200) 50%,
      var(--gray-300) 55%,
      var(--gray-700) 60%,
      var(--gray-700) 100%
    );
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: waveFlash 2s linear infinite;
  }
}

@keyframes waveFlash {
  0% {
    background-position: 200% center;
  }
  100% {
    background-position: -200% center;
  }
}

@media (max-width: 768px) {
  .chat-header .header__left .text {
    display: none;
  }

  .hero-features {
    grid-template-columns: 1fr;
  }

  .example-grid {
    grid-template-columns: 1fr;
  }

  .hero-head {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}
</style>

<style lang="less">
.agent-nav-btn {
  display: flex;
  gap: 6px;
  padding: 6px 8px;
  height: 32px;
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

  &:hover:not(.is-disabled) {
    background-color: var(--gray-100);
  }

  &.is-disabled {
    cursor: not-allowed;
    opacity: 0.7;
    pointer-events: none;
  }

  .nav-btn-icon {
    height: 18px;
  }

  .loading-icon {
    animation: spin 1s linear infinite;
  }
}

.hide-text {
  display: none;
}

@media (min-width: 769px) {
  .hide-text {
    display: inline;
  }
}

/* AgentState 按钮有内容时的样式 */
.agent-nav-btn.agent-state-btn.has-content:hover:not(.is-disabled) {
  color: var(--main-700);
  background-color: var(--main-20);
}

.agent-nav-btn.agent-state-btn.active {
  color: var(--main-700);
  background-color: var(--main-20);
}
</style>

<style lang="less">
#app-router-view {
  background: transparent !important;
}

/* ========== Dark Mode Overrides ========== */
:root.dark #app-router-view {
  background: #0a0a0a !important;
}

:root.dark .chat-container {
  background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('/zj-bjd.png') !important;
  background-size: cover !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
}

:root.dark .bottom {
  background: linear-gradient(180deg, transparent 0%, rgba(10, 10, 10, 0.95) 40%) !important;
}

:root.dark .input-dock .input-box {
  background: rgba(30, 30, 30, 0.95) !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
}

:root.dark .mode-slider {
  background: rgba(30, 30, 30, 0.7) !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
}

:root.dark .start-tag {
  background: rgba(30, 30, 30, 0.6) !important;
  border-color: rgba(74, 175, 78, 0.15) !important;
}

:root.dark .start-prompts {
  background: rgba(30, 30, 30, 0.5) !important;
  border-color: rgba(255, 255, 255, 0.06) !important;
}

:root.dark .start-prompt {
  background: rgba(40, 40, 40, 0.5) !important;
  color: var(--gray-700) !important;
}

:root.dark .start-prompt:hover {
  background: rgba(50, 50, 50, 0.8) !important;
  color: var(--main-500) !important;
}

:root.dark .start-note {
  color: var(--gray-500) !important;
}

:root.dark .agent-panel-wrapper {
  background: var(--gray-10) !important;
  border-color: var(--gray-150) !important;
}

:root.dark .chat-sidebar {
  background: rgba(10, 10, 10, 0.75) !important;
  backdrop-filter: blur(16px) !important;
}

/* Tool call cards */
:root.dark .tool-call-display {
  background: var(--gray-10) !important;
  outline-color: var(--gray-150) !important;
}
</style>
