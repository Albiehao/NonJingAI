<template>
  <div class="chat-bot" :class="{ 'light-mode': isLightMode, open: isOpen }">
    <button
      class="chat-trigger"
      :class="{ active: isOpen }"
      type="button"
      :title="isOpen ? '关闭智能助手' : '打开智能助手'"
      aria-label="智能助手"
      @click="toggleChat"
    >
      <img class="trigger-logo" src="/img/logo.png" alt="品牌标志" />
    </button>

    <transition name="chat-slide">
      <section v-if="isOpen" class="chat-window" aria-label="农业智能助手">
        <header class="chat-header">
          <div class="header-main">
            <div class="header-avatar">
              <img src="/img/logo.png" alt="品牌标志" />
            </div>
            <div class="header-copy">
              <p class="header-kicker">HEXIN AGRI SERVICE</p>
              <h3 class="header-title">农业智能助手</h3>
              <p class="header-status">在线，可连续对话</p>
            </div>
          </div>
          <button class="chat-close" type="button" @click="closeChat">关闭</button>
        </header>

        <div class="chat-messages" ref="messagesContainer">
          <section v-if="messages.length === 0 && !isStreaming" class="chat-welcome">
            <div class="welcome-head">
              <img class="welcome-logo" src="/img/logo.png" alt="品牌标志" />
              <div>
                <p class="welcome-kicker">欢迎使用</p>
                <h4 class="welcome-title">农资推荐、种植问答、商品检索</h4>
              </div>
            </div>
            <p class="welcome-desc">
              你可以直接问我“玉米除草剂推荐”“水稻病虫害怎么防治”“帮我找适合番茄的产品”。
            </p>
            <div class="welcome-grid">
              <div class="welcome-card">
                <span class="welcome-index">01</span>
                <p>按作物推荐农资产品</p>
              </div>
              <div class="welcome-card">
                <span class="welcome-index">02</span>
                <p>解答施肥、病虫害与种植问题</p>
              </div>
              <div class="welcome-card">
                <span class="welcome-index">03</span>
                <p>识别商品并跳转详情页</p>
              </div>
            </div>
          </section>

          <article
            v-for="(msg, index) in messages"
            :key="index"
            class="chat-message"
            :class="msg.type"
          >
            <div class="message-avatar" :class="msg.type">
              <img v-if="msg.type === 'bot'" src="/img/logo.png" alt="品牌标志" />
              <span v-else>我</span>
            </div>
            <div class="message-body">
              <div class="message-label">{{ msg.type === 'user' ? '我的提问' : '助手回复' }}</div>
              <div class="message-shell">
                <div class="message-text" v-html="formatMessage(msg.text)"></div>
                <div v-if="msg.recommendations && msg.recommendations.length > 0" class="recommendations">
                  <div class="recommendations-title">推荐农资</div>
                  <button
                    v-for="product in msg.recommendations"
                    :key="product.productId"
                    class="product-card"
                    type="button"
                    @click="goToProduct(product.productId)"
                  >
                    <div class="product-image-wrap">
                      <img
                        v-if="product.mainImage"
                        class="product-image"
                        :src="product.mainImage"
                        :alt="product.productName"
                      />
                      <div v-else class="product-image-placeholder">暂无图片</div>
                    </div>
                    <div class="product-card-main">
                      <span class="product-name">{{ product.productName }}</span>
                      <span v-if="product.price" class="product-price">{{ product.price }} 元</span>
                    </div>
                    <span class="product-arrow">查看</span>
                  </button>
                </div>
              </div>
            </div>
          </article>

          <article v-if="isStreaming" class="chat-message bot streaming">
            <div class="message-avatar bot">
              <img src="/img/logo.png" alt="品牌标志" />
            </div>
            <div class="message-body">
              <div class="message-label">助手回复</div>
              <div class="message-shell">
                <div v-if="streamingMessage" class="message-text" v-html="formatMessage(streamingMessage)"></div>
                <div v-else class="message-pending">正在生成回答...</div>
                <span class="streaming-indicator"></span>
                <div
                  v-if="streamingRecommendations && streamingRecommendations.length > 0"
                  class="recommendations"
                >
                  <div class="recommendations-title">推荐农资</div>
                  <button
                    v-for="product in streamingRecommendations"
                    :key="product.productId"
                    class="product-card"
                    type="button"
                    @click="goToProduct(product.productId)"
                  >
                    <div class="product-image-wrap">
                      <img
                        v-if="product.mainImage"
                        class="product-image"
                        :src="product.mainImage"
                        :alt="product.productName"
                      />
                      <div v-else class="product-image-placeholder">暂无图片</div>
                    </div>
                    <div class="product-card-main">
                      <span class="product-name">{{ product.productName }}</span>
                      <span v-if="product.price" class="product-price">{{ product.price }} 元</span>
                    </div>
                    <span class="product-arrow">查看</span>
                  </button>
                </div>
              </div>
            </div>
          </article>

          <article v-if="isLoading && !isStreaming" class="chat-message bot">
            <div class="message-avatar bot">
              <img src="/img/logo.png" alt="品牌标志" />
            </div>
            <div class="message-body">
              <div class="message-label">助手回复</div>
              <div class="message-shell">
                <div class="message-pending">正在请求响应...</div>
              </div>
            </div>
          </article>
        </div>

        <footer class="chat-input-area">
          <textarea
            v-model="inputMessage"
            class="chat-input"
            rows="1"
            placeholder="请输入你的问题，例如：帮我推荐适合玉米的除草剂"
            :disabled="isLoading || isStreaming"
            @keydown.enter.exact.prevent="sendMessage"
          ></textarea>
          <button
            class="chat-send"
            type="button"
            :disabled="!inputMessage.trim() || isLoading || isStreaming"
            @click="sendMessage"
          >
            发送
          </button>
        </footer>
      </section>
    </transition>
  </div>
</template>

<script>
import { chat, chatStream } from '@/api/chat'

export default {
  name: 'ChatBot',
  props: {
    isLightMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isOpen: false,
      inputMessage: '',
      messages: [],
      isLoading: false,
      isStreaming: false,
      streamingMessage: '',
      streamingRecommendations: []
    }
  },
  mounted() {
    window.chatBotNavigate = this.goToProduct
  },
  beforeDestroy() {
    window.chatBotNavigate = null
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen
    },
    closeChat() {
      this.isOpen = false
    },
    async sendMessage() {
      if (!this.inputMessage.trim() || this.isLoading || this.isStreaming) return

      const userMessage = this.inputMessage.trim()
      this.messages.push({ type: 'user', text: userMessage })
      this.inputMessage = ''
      this.isLoading = true
      this.scrollToBottom()

      const timeoutId = setTimeout(() => {
        if (this.isLoading || this.isStreaming) {
          this.tryNonStreamingFallback(userMessage)
        }
      }, 30000)

      try {
        this.isStreaming = true
        this.streamingMessage = ''
        this.streamingRecommendations = []
        this.isLoading = false

        await chatStream(userMessage, {
          onToken: (token) => {
            this.streamingMessage += token
            this.scrollToBottom()
          },
          onRecommendations: (recommendations) => {
            if (recommendations && recommendations.length > 0) {
              this.streamingRecommendations = recommendations
              this.scrollToBottom()
            }
          },
          onComplete: () => {
            clearTimeout(timeoutId)
            this.finalizeStreamingMessage()
          },
          onError: () => {
            clearTimeout(timeoutId)
          }
        })

        clearTimeout(timeoutId)
        if (this.isStreaming) {
          this.finalizeStreamingMessage()
        }
      } catch (error) {
        clearTimeout(timeoutId)
        this.tryNonStreamingFallback(userMessage)
      }
    },
    finalizeStreamingMessage() {
      if (this.streamingMessage || (this.streamingRecommendations && this.streamingRecommendations.length > 0)) {
        this.messages.push({
          type: 'bot',
          text: this.streamingMessage,
          recommendations: this.streamingRecommendations
        })
      }
      this.isStreaming = false
      this.isLoading = false
      this.streamingMessage = ''
      this.streamingRecommendations = []
      this.scrollToBottom()
    },
    async tryNonStreamingFallback(userMessage) {
      this.isStreaming = false
      this.streamingMessage = ''
      this.isLoading = true

      try {
        const res = await chat(userMessage)
        if (res.code === 0) {
          this.messages.push({
            type: 'bot',
            text: res.data.reply,
            recommendations: res.data.recommendations || []
          })
        } else {
          this.messages.push({
            type: 'bot',
            text: '当前服务暂时不可用，请稍后再试。'
          })
        }
      } catch (fallbackError) {
        this.messages.push({
          type: 'bot',
          text: '网络异常，请检查连接后重试。'
        })
      } finally {
        this.isLoading = false
        this.isStreaming = false
        this.streamingMessage = ''
        this.streamingRecommendations = []
        this.scrollToBottom()
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    },
    formatMessage(text) {
      if (!text) return ''
      let html = this.parseMarkdown(text)
      html = html.replace(/\/products\/(\d+)/g, (match, id) => {
        return `<a href="#" class="md-link product-text-link" data-product-id="${id}" onclick="window.chatBotNavigate && window.chatBotNavigate(${id}); return false;">${match}</a>`
      })
      return html
    },
    parseMarkdown(text) {
      let html = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')

      html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre class="md-code-block"><code>${code.trim()}</code></pre>`
      })

      html = html.replace(/`([^`]+)`/g, '<code class="md-inline-code">$1</code>')
      html = html.replace(/^### (.+)$/gm, '<h3 class="md-h3">$1</h3>')
      html = html.replace(/^## (.+)$/gm, '<h2 class="md-h2">$1</h2>')
      html = html.replace(/^# (.+)$/gm, '<h1 class="md-h1">$1</h1>')
      html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
      html = html.replace(/\*\*(.+?)\*\*/g, '<strong class="md-bold">$1</strong>')
      html = html.replace(/\*(.+?)\*/g, '<em class="md-italic">$1</em>')
      html = html.replace(/___(.+?)___/g, '<strong><em>$1</em></strong>')
      html = html.replace(/__(.+?)__/g, '<strong class="md-bold">$1</strong>')
      html = html.replace(/_(.+?)_/g, '<em class="md-italic">$1</em>')
      html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="md-link">$1</a>')
      html = html.replace(/^[*\-+] (.+)$/gm, '<li class="md-li">$1</li>')
      html = html.replace(/(<li class="md-li">.*<\/li>\n?)+/g, (m) => `<ul class="md-ul">${m}</ul>`)
      html = html.replace(/^\d+\. (.+)$/gm, '<li class="md-li-ol">$1</li>')
      html = html.replace(/(<li class="md-li-ol">.*<\/li>\n?)+/g, (m) => `<ol class="md-ol">${m}</ol>`)
      html = html.replace(/^---$/gm, '<hr class="md-hr">')
      html = html.replace(/^\*\*\*$/gm, '<hr class="md-hr">')
      html = html.replace(/^&gt; (.+)$/gm, '<blockquote class="md-quote">$1</blockquote>')

      const lines = html.split('\n')
      const result = []
      let paragraphBuffer = []

      for (let line of lines) {
        line = line.trim()
        if (line === '') {
          if (paragraphBuffer.length > 0) {
            result.push(`<p class="md-p">${paragraphBuffer.join(' ')}</p>`)
            paragraphBuffer = []
          }
          continue
        }

        if (line.match(/^<(h[1-6]|ul|ol|li|pre|blockquote|hr|p)/)) {
          if (paragraphBuffer.length > 0) {
            result.push(`<p class="md-p">${paragraphBuffer.join(' ')}</p>`)
            paragraphBuffer = []
          }
          result.push(line)
        } else {
          paragraphBuffer.push(line)
        }
      }

      if (paragraphBuffer.length > 0) {
        result.push(`<p class="md-p">${paragraphBuffer.join(' ')}</p>`)
      }

      return result.join('\n')
    },
    goToProduct(productId) {
      const targetPath = `/products/${productId}`
      if (this.$route.path === targetPath) {
        this.closeChat()
        return
      }
      this.$router.push(targetPath).catch(() => {})
      this.closeChat()
    }
  }
}
</script>

<style scoped>
.chat-bot {
  --chat-panel: rgba(23, 28, 40, 0.94);
  --chat-shell: #252c3a;
  --chat-shell-soft: #2f384a;
  --chat-line: #65462a;
  --chat-line-soft: #8d6b4b;
  --chat-text: #f7e5be;
  --chat-muted: #c2b295;
  --chat-accent: #ffd46a;
  --chat-bot-bubble: #273847;
  --chat-user-bubble: #6f4c30;
  position: relative;
  z-index: 31;
  color: var(--chat-text);
  font-family: 'Courier New', 'Lucida Console', monospace;
}

.chat-bot.light-mode {
  --chat-panel: rgba(250, 242, 230, 0.96);
  --chat-shell: #f8f0e2;
  --chat-shell-soft: #efe3d1;
  --chat-line: #9a7348;
  --chat-line-soft: #6f4c30;
  --chat-text: #3f2c1f;
  --chat-muted: #5d4f43;
  --chat-accent: #9d621f;
  --chat-bot-bubble: #f3e7d5;
  --chat-user-bubble: #7e5936;
}

.chat-trigger {
  width: 50px;
  height: 50px;
  padding: 0;
  border: 2px solid var(--chat-line);
  background: var(--chat-shell-soft);
  color: var(--chat-text);
  box-shadow: 0 4px 0 rgba(8, 10, 15, 0.42);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.16s ease, filter 0.2s ease, box-shadow 0.2s ease;
}

.chat-trigger:hover {
  filter: brightness(1.06);
}

.chat-trigger:active {
  transform: translateY(2px);
  box-shadow: 0 2px 0 rgba(8, 10, 15, 0.42);
}

.chat-trigger.active {
  border-color: var(--chat-line-soft);
}

.trigger-logo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.chat-window {
  position: absolute;
  right: 0;
  bottom: 66px;
  width: min(410px, calc(100vw - 32px));
  height: min(640px, calc(100vh - 180px));
  border: 2px solid var(--chat-line);
  background:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    var(--chat-panel);
  background-size: 8px 8px, 8px 8px, auto;
  box-shadow: inset 0 2px 0 rgba(255, 255, 255, 0.08), 0 10px 0 rgba(8, 10, 15, 0.42);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  padding: 14px;
  border-bottom: 2px solid var(--chat-line);
  background: rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.header-avatar {
  width: 46px;
  height: 46px;
  border: 2px solid var(--chat-line);
  background: var(--chat-shell);
  overflow: hidden;
  flex-shrink: 0;
}

.header-avatar img,
.welcome-logo,
.message-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.header-kicker {
  font-size: 10px;
  letter-spacing: 1.4px;
  color: var(--chat-accent);
}

.header-title {
  margin-top: 4px;
  font-size: 18px;
}

.header-status {
  margin-top: 4px;
  font-size: 11px;
  color: var(--chat-muted);
}

.chat-close {
  min-width: 64px;
  height: 34px;
  padding: 0 10px;
  border: 2px solid var(--chat-line);
  background: var(--chat-shell-soft);
  color: var(--chat-text);
  font: inherit;
  font-size: 11px;
  cursor: pointer;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: var(--chat-line);
}

.chat-welcome {
  border: 2px solid var(--chat-line);
  background: var(--chat-shell);
  box-shadow: 0 4px 0 rgba(8, 10, 15, 0.22);
  padding: 14px;
}

.welcome-head {
  display: flex;
  align-items: center;
  gap: 12px;
}

.welcome-logo {
  width: 48px;
  height: 48px;
  border: 2px solid var(--chat-line);
  background: rgba(0, 0, 0, 0.12);
  flex-shrink: 0;
}

.welcome-kicker {
  color: var(--chat-accent);
  font-size: 11px;
  letter-spacing: 1.4px;
}

.welcome-title {
  margin-top: 6px;
  font-size: 15px;
  line-height: 1.5;
}

.welcome-desc {
  margin-top: 10px;
  color: var(--chat-muted);
  font-size: 12px;
  line-height: 1.7;
}

.welcome-grid {
  margin-top: 12px;
  display: grid;
  gap: 8px;
}

.welcome-card {
  border: 1px solid var(--chat-line);
  background: rgba(0, 0, 0, 0.08);
  padding: 10px 12px;
  display: grid;
  grid-template-columns: 34px 1fr;
  gap: 10px;
  align-items: start;
}

.welcome-index {
  color: var(--chat-accent);
  font-size: 11px;
}

.welcome-card p {
  font-size: 12px;
  line-height: 1.6;
}

.chat-message {
  display: flex;
  gap: 10px;
  align-items: flex-start;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 34px;
  height: 34px;
  border: 2px solid var(--chat-line);
  background: var(--chat-shell-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
  font-size: 12px;
  font-weight: 700;
}

.message-body {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: calc(100% - 44px);
}

.chat-message.user .message-body {
  align-items: flex-end;
}

.message-label {
  font-size: 10px;
  letter-spacing: 1.2px;
  color: var(--chat-muted);
}

.message-shell {
  width: fit-content;
  max-width: 100%;
  border: 2px solid var(--chat-line);
  box-shadow: 0 4px 0 rgba(8, 10, 15, 0.18);
  padding: 10px 12px;
}

.chat-message.bot .message-shell {
  background: var(--chat-bot-bubble);
}

.chat-message.user .message-shell {
  background: var(--chat-user-bubble);
  color: #fff6e5;
}

.message-text,
.message-pending {
  font-size: 12px;
  line-height: 1.7;
  word-break: break-word;
}

.message-pending {
  color: var(--chat-muted);
}

.recommendations {
  margin-top: 12px;
  display: grid;
  gap: 8px;
}

.recommendations-title {
  font-size: 11px;
  color: var(--chat-accent);
  letter-spacing: 1.2px;
}

.product-card {
  width: 100%;
  border: 2px solid var(--chat-line);
  background: var(--chat-shell);
  color: var(--chat-text);
  padding: 8px;
  display: grid;
  grid-template-columns: 58px 1fr auto;
  gap: 10px;
  align-items: center;
  cursor: pointer;
  text-align: left;
}

.product-card:hover {
  filter: brightness(1.04);
}

.product-image-wrap {
  width: 58px;
  height: 58px;
  border: 2px solid var(--chat-line);
  background: rgba(0, 0, 0, 0.12);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-image-placeholder {
  padding: 4px;
  font-size: 10px;
  line-height: 1.4;
  color: var(--chat-muted);
  text-align: center;
}

.product-card-main {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.product-name {
  font-size: 13px;
  color: inherit;
}

.product-price {
  font-size: 11px;
  color: var(--chat-accent);
}

.product-arrow {
  font-size: 11px;
  color: var(--chat-muted);
}

.streaming-indicator {
  display: inline-block;
  width: 8px;
  height: 12px;
  margin-top: 8px;
  background: var(--chat-accent);
  animation: blink 0.8s infinite;
}

.chat-input-area {
  border-top: 2px solid var(--chat-line);
  padding: 12px;
  background: rgba(0, 0, 0, 0.08);
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
}

.chat-input {
  min-height: 72px;
  max-height: 140px;
  resize: none;
  border: 2px solid var(--chat-line);
  background: var(--chat-shell);
  color: var(--chat-text);
  padding: 10px 12px;
  font: inherit;
  font-size: 12px;
  line-height: 1.6;
  outline: none;
}

.chat-input::placeholder {
  color: var(--chat-muted);
}

.chat-input:focus {
  border-color: var(--chat-line-soft);
}

.chat-send {
  min-width: 78px;
  border: 2px solid var(--chat-line);
  background: var(--chat-shell-soft);
  color: var(--chat-text);
  font: inherit;
  font-size: 12px;
  cursor: pointer;
}

.chat-send:disabled,
.chat-input:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.message-text .md-h1,
.message-text .md-h2,
.message-text .md-h3 {
  margin: 8px 0 6px;
  color: var(--chat-accent);
}

.message-text .md-italic {
  color: var(--chat-muted);
}

.message-text .md-link {
  color: var(--chat-accent);
  text-decoration: none;
  border-bottom: 1px solid currentColor;
}

.message-text .md-inline-code {
  padding: 1px 4px;
  border: 1px solid var(--chat-line);
  background: rgba(0, 0, 0, 0.14);
}

.message-text .md-code-block {
  margin: 8px 0;
  padding: 10px;
  border: 1px solid var(--chat-line);
  background: rgba(0, 0, 0, 0.12);
  overflow-x: auto;
}

.message-text .md-ul,
.message-text .md-ol {
  margin: 6px 0;
  padding-left: 18px;
}

.message-text .md-quote {
  margin: 8px 0;
  padding: 8px 10px;
  border-left: 2px solid var(--chat-accent);
  background: rgba(0, 0, 0, 0.08);
}

.message-text .md-hr {
  margin: 10px 0;
  border: none;
  border-top: 1px solid var(--chat-line);
}

.message-text .md-p {
  margin: 0;
}

.chat-slide-enter-active,
.chat-slide-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.chat-slide-enter,
.chat-slide-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

@media (max-width: 768px) {
  .chat-window {
    width: min(410px, calc(100vw - 24px));
    height: min(72vh, 560px);
  }

  .product-card {
    grid-template-columns: 52px 1fr;
  }

  .product-arrow {
    display: none;
  }
}
</style>
