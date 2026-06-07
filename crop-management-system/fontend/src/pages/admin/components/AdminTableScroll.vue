<template>
  <div class="admin-scroll-area">
    <div ref="viewport" class="admin-scroll-viewport" @scroll="syncThumb">
      <slot></slot>
    </div>
    <div v-show="trackVisible" ref="track" class="admin-scroll-track" @mousedown="onTrackDown">
      <div
        class="admin-scroll-thumb"
        :style="{ width: `${thumbWidth}px`, transform: `translateX(${thumbLeft}px)` }"
        @mousedown.stop="onThumbDown"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminTableScroll',
  data() {
    return {
      trackVisible: false,
      thumbWidth: 0,
      thumbLeft: 0,
      dragging: false,
      dragStartX: 0,
      dragStartLeft: 0,
      resizeObserver: null
    }
  },
  mounted() {
    this.updateThumb()
    this.resizeObserver = new ResizeObserver(() => this.updateThumb())
    this.resizeObserver.observe(this.$refs.viewport)
    window.addEventListener('resize', this.updateThumb)
    window.addEventListener('mousemove', this.onDragMove)
    window.addEventListener('mouseup', this.onDragEnd)
  },
  beforeDestroy() {
    if (this.resizeObserver) this.resizeObserver.disconnect()
    window.removeEventListener('resize', this.updateThumb)
    window.removeEventListener('mousemove', this.onDragMove)
    window.removeEventListener('mouseup', this.onDragEnd)
  },
  methods: {
    updateThumb() {
      const viewport = this.$refs.viewport
      const track = this.$refs.track
      if (!viewport || !track) return

      const { scrollWidth, clientWidth, scrollLeft } = viewport
      this.trackVisible = scrollWidth > clientWidth + 1
      if (!this.trackVisible) {
        this.thumbWidth = 0
        this.thumbLeft = 0
        return
      }

      const trackWidth = track.clientWidth
      const ratio = clientWidth / scrollWidth
      this.thumbWidth = Math.max(48, Math.round(trackWidth * ratio))
      const maxThumbLeft = Math.max(0, trackWidth - this.thumbWidth)
      const maxScrollLeft = Math.max(1, scrollWidth - clientWidth)
      this.thumbLeft = Math.round((scrollLeft / maxScrollLeft) * maxThumbLeft)
    },
    syncThumb() {
      this.updateThumb()
    },
    onThumbDown(event) {
      this.dragging = true
      this.dragStartX = event.clientX
      this.dragStartLeft = this.thumbLeft
    },
    onDragMove(event) {
      if (!this.dragging) return
      const viewport = this.$refs.viewport
      const track = this.$refs.track
      if (!viewport || !track) return

      const maxThumbLeft = Math.max(0, track.clientWidth - this.thumbWidth)
      const delta = event.clientX - this.dragStartX
      const nextThumbLeft = Math.min(maxThumbLeft, Math.max(0, this.dragStartLeft + delta))
      this.thumbLeft = nextThumbLeft

      const maxScrollLeft = Math.max(0, viewport.scrollWidth - viewport.clientWidth)
      viewport.scrollLeft = maxThumbLeft > 0 ? (nextThumbLeft / maxThumbLeft) * maxScrollLeft : 0
    },
    onDragEnd() {
      this.dragging = false
    },
    onTrackDown(event) {
      const track = this.$refs.track
      const viewport = this.$refs.viewport
      if (!track || !viewport) return
      const rect = track.getBoundingClientRect()
      const clickX = event.clientX - rect.left
      const targetLeft = clickX - this.thumbWidth / 2
      const maxThumbLeft = Math.max(0, track.clientWidth - this.thumbWidth)
      const nextThumbLeft = Math.min(maxThumbLeft, Math.max(0, targetLeft))
      const maxScrollLeft = Math.max(0, viewport.scrollWidth - viewport.clientWidth)
      viewport.scrollLeft = maxThumbLeft > 0 ? (nextThumbLeft / maxThumbLeft) * maxScrollLeft : 0
      this.updateThumb()
    }
  }
}
</script>

<style scoped>
.admin-scroll-area {
  width: 100%;
  position: relative;
  padding-bottom: 10px;
}

.admin-scroll-viewport {
  overflow-x: auto;
  overflow-y: hidden;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.admin-scroll-viewport::-webkit-scrollbar {
  width: 0;
  height: 0;
  display: none;
}

.admin-scroll-track {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 6px;
  border: 1px solid rgba(101, 70, 42, 0.8);
  background: rgba(37, 44, 58, 0.82);
  cursor: pointer;
  opacity: 0.85;
}

.admin-scroll-thumb {
  position: absolute;
  top: 0;
  left: 0;
  height: calc(100% - 2px);
  top: 1px;
  background: linear-gradient(180deg, #ffd46a, #8b652f);
  border: 1px solid #6c4d26;
  box-sizing: border-box;
  cursor: grab;
}

.admin-scroll-thumb:active {
  cursor: grabbing;
}

.admin-page.light-mode .admin-scroll-track {
  background: rgba(248, 240, 226, 0.92);
  border-color: rgba(154, 115, 72, 0.9);
}

.admin-page.light-mode .admin-scroll-thumb {
  background: linear-gradient(180deg, #d8b387, #b38452);
  border-color: #8c6846;
}
</style>
