<template>
  <div class="radio-panel">
    <!-- 旋钮容器 -->
    <div 
      class="knob-wrapper"
      :style="{ transform: `rotate(${rotation}deg)` }"
      @mousedown="startDrag"
      @mouseenter="isHovering = true"
      @mouseleave="isHovering = false"
    >
      <!-- 旋钮主体 -->
      <div class="knob-body">
        <!-- 刻度环 -->
        <div class="scale-ring">
          <div 
            v-for="(tick, index) in ticks" 
            :key="index"
            class="tick"
            :class="{ 'major': tick.isMajor }"
            :style="{ transform: `rotate(${tick.angle}deg)` }"
          ></div>
        </div>

        <!-- 指针 -->
        <div class="pointer"></div>

        <!-- 中心装饰盖 -->
        <div class="center-cap"></div>
      </div>
    </div>

    <!-- 数字显示屏 -->
    <div class="display-area">
      <div class="screen">
        <span class="value">{{ displayValue }}</span>
        <span class="unit">MHz</span>
      </div>
      <div class="brand-label">RETRO RADIO</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VintageKnob',
  
  // 1. Props 定义 (替代 defineProps)
  props: {
    modelValue: {
      type: Number,
      default: 98.0
    },
    min: {
      type: Number,
      default: 87.5
    },
    max: {
      type: Number,
      default: 108.0
    },
    totalTicks: {
      type: Number,
      default: 100
    }
  },

  data() {
    return {
      rotation: 0,
      isDragging: false,
      startX: 0,
      startRotation: 0
    };
  },

  computed: {
    // 计算属性组 (替代 computed: () => {})
    valueRange() {
      return this.max - this.min;
    },

    displayValue() {
      const normalizedRot = ((this.rotation % 360) + 360) % 360;
      const percentage = normalizedRot / 360;
      return (this.min + percentage * this.valueRange).toFixed(1);
    },

    ticks() {
      const list = [];
      const stepAngle = 360 / this.totalTicks;
      
      for (let i = 0; i <= this.totalTicks; i++) {
        const angle = i * stepAngle;
        const isMajor = i % 10 === 0;
        list.push({ angle, isMajor });
      }
      return list;
    }
  },

  methods: {
    // 2. 方法定义 (替代 script setup 中的函数)
    
    snapToGrid() {
      let currentDeg = this.rotation % 360;
      if (currentDeg < 0) currentDeg += 360;

      const stepDeg = 360 / this.totalTicks;
      const snappedIndex = Math.round(currentDeg / stepDeg);
      const snappedDeg = snappedIndex * stepDeg;
      
      this.rotation = snappedDeg;
    },

    getCurrentValue() {
      const normalizedRot = ((this.rotation % 360) + 360) % 360;
      const percentage = normalizedRot / 360;
      return this.min + percentage * this.valueRange;
    },

    startDrag(e) {
      e.preventDefault();
      this.isDragging = true;
      this.startX = e.clientX;
      this.startRotation = this.rotation;
      
      document.addEventListener('mousemove', this.handleDrag);
      document.addEventListener('mouseup', this.stopDrag);
    },

    handleDrag(e) {
      if (!this.isDragging) return;
      
      const deltaX = e.clientX - this.startX;
      const sensitivity = 0.4; 
      this.rotation = this.startRotation + deltaX * sensitivity;
    },

    stopDrag() {
      if (!this.isDragging) return;
      this.isDragging = false;
      
      document.removeEventListener('mousemove', this.handleDrag);
      document.removeEventListener('mouseup', this.stopDrag);
      
      this.snapToGrid();
      
      // 触发 v-model 更新 (替代 emit)
      this.$emit('update:modelValue', this.getCurrentValue());
    }
  },

  mounted() {
    // 3. 生命周期钩子 (替代 onMounted)
    let targetVal = this.modelValue;
    if (targetVal < this.min) targetVal = this.min;
    if (targetVal > this.max) targetVal = this.max;

    const percentage = (targetVal - this.min) / this.valueRange;
    this.rotation = percentage * 360;
  },

  beforeDestroy() {
    // 4. 销毁时清理 (替代 onUnmounted)
    document.removeEventListener('mousemove', this.handleDrag);
    document.removeEventListener('mouseup', this.stopDrag);
  }
};
</script>

<style scoped>
/* CSS 样式保持不变 */
.radio-panel {
  position: relative;
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #2b1d1a 0%, #1a1210 100%);
  border-radius: 24px;
  box-shadow: 
    inset 0 0 40px rgba(0,0,0,0.9),
    0 15px 30px rgba(0,0,0,0.6),
    0 0 0 10px #5d4037;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  user-select: none;
  overflow: hidden;
}

.knob-wrapper {
  position: relative;
  width: 160px;
  height: 160px;
  cursor: grab;
  transition: transform 0.1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  z-index: 10;
}

.knob-wrapper:active {
  cursor: grabbing;
  transition: none;
}

.knob-body {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, #6d4c41, #4e342e, #281815);
  box-shadow: 
    0 10px 25px rgba(0,0,0,0.7),
    inset 0 0 0 3px #8d6e63,
    inset 0 0 30px rgba(0,0,0,0.8);
  position: relative;
  overflow: hidden;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.1'/%3E%3C/svg%3E");
}

.scale-ring {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  border-radius: 50%;
  pointer-events: none;
}

.tick {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 2px;
  height: 8px;
  background: #d7ccc8;
  transform-origin: 0 0;
  box-shadow: 0 1px 2px rgba(0,0,0,0.5);
}

.tick.major {
  height: 14px;
  width: 3px;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.6);
}

.pointer {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 4px;
  height: 75px;
  background: linear-gradient(to bottom, #ffeb3b, #fbc02d);
  transform-origin: 50% 100%;
  transform: translate(-50%, -100%) rotate(0deg);
  border-radius: 2px;
  z-index: 20;
  box-shadow: 0 0 5px rgba(255, 235, 59, 0.6);
}

.center-cap {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40px;
  height: 40px;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, #8d6e63, #4e342e);
  box-shadow: 0 3px 8px rgba(0,0,0,0.6);
  z-index: 30;
  border: 1px solid #6d4c41;
}

.display-area {
  margin-top: 40px;
  text-align: center;
}

.screen {
  padding: 8px 24px;
  background: #000;
  border: 2px solid #5d4037;
  border-radius: 6px;
  font-size: 28px;
  color: #ffeb3b;
  text-shadow: 0 0 8px rgba(255, 235, 59, 0.6);
  letter-spacing: 2px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
  box-shadow: inset 0 0 10px rgba(0,0,0,0.9);
  min-width: 120px;
  display: inline-flex;
  align-items: baseline;
}

.unit {
  font-size: 14px;
  color: #ffeb3b;
  margin-left: 5px;
  opacity: 0.8;
}

.brand-label {
  margin-top: 12px;
  font-size: 12px;
  color: #8d6e63;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: bold;
}
</style>