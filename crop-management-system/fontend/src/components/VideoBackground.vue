<template>
  <div class="video-bg" aria-hidden="true">
    <video
      class="video-bg__media"
      :src="src"
      muted
      autoplay
      loop
      playsinline
    />
  </div>
</template>

<script>
import bgVideo from '../assets/veadio/background.mp4'

export default {
  name: 'VideoBackground',
  data() {
    return {
      src: bgVideo
    }
  }
}
</script>

<style scoped>
.video-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.video-bg__media {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
