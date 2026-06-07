<template>
  <MessageInputComponent
    ref="inputRef"
    :key="inputKey"
    :model-value="modelValue"
    @update:modelValue="updateValue"
    :is-loading="isLoading"
    :disabled="disabled"
    :send-button-disabled="sendButtonDisabled"
    :placeholder="placeholder"
    :force-multi-line="hasStateContent"
    :mention="mention"
    @send="handleSend"
    @keydown="handleKeyDown"
  >
    <template #top>
      <ImagePreviewComponent
        v-if="currentImage"
        :image-data="currentImage"
        @remove="handleImageRemoved"
        class="image-preview-wrapper"
      />
    </template>
    <template #actions-left>
      <div class="input-actions-left">
        <!-- Image Upload Button -->
        <div
          v-if="supportsFileUpload"
          class="action-btn"
          :class="{ disabled }"
          @click="handleImageUploadClick"
          title="上传图片"
        >
          <Image :size="16" />
        </div>
        <!-- Document Upload Button -->
        <div
          v-if="supportsFileUpload"
          class="action-btn"
          :class="{ disabled }"
          @click="handleFileInputClick"
          title="上传文档"
        >
          <FileText :size="16" />
        </div>
        <input
          ref="fileInputRef"
          type="file"
          multiple
          accept=".txt,.md,.docx,.html,.htm"
          :disabled="disabled"
          @change="handleFileChange"
          style="display: none"
        />
        <!-- State Toggle Button -->
        <div
          v-if="hasStateContent"
          class="state-toggle-btn"
          :class="{ active: isPanelOpen }"
          @click="$emit('toggle-panel')"
          title="查看工作状态"
        >
          <FolderCode :size="14" />
          <span>状态</span>
        </div>
      </div>
    </template>
  </MessageInputComponent>
</template>

<script setup>
import { ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import MessageInputComponent from '@/components/MessageInputComponent.vue'
import ImagePreviewComponent from '@/components/ImagePreviewComponent.vue'
import { threadApi, multimodalApi } from '@/apis'
import { AgentValidator } from '@/utils/agentValidator'
import { handleChatError, handleValidationError } from '@/utils/errorHandler'
import { FolderCode, Image, FileText } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: String, default: '' },
  isLoading: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  sendButtonDisabled: { type: Boolean, default: false },
  placeholder: { type: String, default: '输入问题...' },
  supportsFileUpload: { type: Boolean, default: false },
  agentId: { type: String, default: '' },
  threadId: { type: String, default: null },
  ensureThread: { type: Function, required: true },
  hasStateContent: { type: Boolean, default: false },
  isPanelOpen: { type: Boolean, default: false },
  mention: { type: Object, default: () => null }
})

const emit = defineEmits([
  'update:modelValue',
  'send',
  'keydown',
  'attachment-changed',
  'toggle-panel'
])

const inputRef = ref(null)
const fileInputRef = ref(null)
const currentImage = ref(null)

// 用于强制重建输入组件的 key
const inputKey = ref(0)

// 监听 hasStateContent 变化，当从有 state 切换到无 state 时重建组件
watch(
  () => props.hasStateContent,
  (newVal, oldVal) => {
    // 当 hasStateContent 从 true 变为 false 时，重建输入组件
    if (oldVal === true && newVal === false) {
      inputKey.value++
    }
  }
)

const updateValue = (val) => {
  emit('update:modelValue', val)
}

const handleAttachmentUpload = async (files) => {
  if (!files?.length) return
  if (!AgentValidator.validateAgentIdWithError(props.agentId, '上传附件', handleValidationError))
    return

  const preferredTitle = files[0]?.name || '新的对话'
  let threadId = props.threadId

  if (!threadId) {
    try {
      threadId = await props.ensureThread(preferredTitle)
    } catch (e) {
      return
    }
  }

  if (!threadId) {
    message.error('创建对话失败，无法上传附件')
    return
  }

  try {
    const hide = message.loading({
      content: '正在上传附件...',
      key: 'upload-attachment',
      duration: 0
    })
    for (const file of files) {
      await threadApi.uploadThreadAttachment(threadId, file)
    }
    message.success({ content: '附件上传成功', key: 'upload-attachment', duration: 2 })
    emit('attachment-changed', threadId)
  } catch (error) {
    message.destroy('upload-attachment')
    handleChatError(error, 'upload')
  }
}

const handleImageUpload = (imageData) => {
  if (imageData && imageData.success) {
    currentImage.value = imageData
  }
}

const handleImageRemoved = () => {
  currentImage.value = null
}

// Direct file upload button handlers
const handleFileInputClick = () => {
  if (props.disabled) return
  fileInputRef.value?.click()
}

const handleFileChange = (event) => {
  const files = event.target.files
  if (files && files.length > 0) {
    handleAttachmentUpload(Array.from(files))
  }
  event.target.value = ''
}

const handleImageUploadClick = () => {
  if (props.disabled) return
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.multiple = false
  input.style.display = 'none'
  input.onchange = async (event) => {
    const file = event.target.files[0]
    if (file) {
      await processImageUpload(file)
    }
    document.body.removeChild(input)
  }
  document.body.appendChild(input)
  input.click()
}

const processImageUpload = async (file) => {
  try {
    if (file.size > 10 * 1024 * 1024) {
      message.error('图片文件过大，请选择小于10MB的图片')
      return
    }
    if (!file.type.startsWith('image/')) {
      message.error('请选择有效的图片文件')
      return
    }
    message.loading({ content: '正在处理图片...', key: 'image-upload' })
    const result = await multimodalApi.uploadImage(file)
    if (result.success) {
      message.success({ content: '图片处理成功', key: 'image-upload', duration: 2 })
      handleImageUpload({
        success: true,
        imageUrl: result.image_url,
        format: result.format,
        mimeType: result.mime_type || file.type,
        sizeBytes: result.size_bytes,
        originalName: file.name
      })
    } else {
      message.error({ content: `图片处理失败: ${result.error}`, key: 'image-upload' })
    }
  } catch (error) {
    console.error('图片上传失败:', error)
    message.error({ content: `图片上传失败: ${error.message || '未知错误'}`, key: 'image-upload' })
  }
}

const handleSend = () => {
  emit('send', { image: currentImage.value })
  currentImage.value = null
}

const handleKeyDown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  } else {
    emit('keydown', e)
  }
}

defineExpose({
  focus: () => inputRef.value?.focus(),
  closeOptions: () => inputRef.value?.closeOptions()
})
</script>

<style lang="less" scoped>
.input-actions-left {
  display: flex;
  align-items: center;
  gap: 4px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  color: var(--gray-500);
  cursor: pointer;
  transition: all 0.2s ease;
  background: transparent;
  border: none;

  &:hover {
    color: var(--main-color);
    background: var(--gray-100);
  }

  &.disabled {
    opacity: 0.4;
    cursor: not-allowed;
    pointer-events: none;
  }
}

.state-toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 8px;
  height: 28px;
  border-radius: 8px;
  font-size: 13px;
  color: var(--gray-600);
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  background: transparent;
  border: none;

  &:hover {
    color: var(--main-color);
    background: var(--gray-100);
  }

  &.active {
    color: var(--main-color);
    background: var(--main-50);
    font-weight: 500;
  }

  &:active {
    transform: scale(0.95);
  }

  &.disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }

  span {
    line-height: 1;
  }
}
</style>
