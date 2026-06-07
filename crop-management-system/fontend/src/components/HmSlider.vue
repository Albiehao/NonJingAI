<template>
  <div class="retro-slider" :class="{ disabled }">
    <div class="retro-slider__frame">
      <div class="retro-slider__inner">
        <div class="retro-slider__meta">
          <span class="retro-slider__label">{{ label }}</span>
          <span class="retro-slider__value">{{ displayValue }}</span>
        </div>

        <div class="retro-slider__track-wrap">
          <div class="retro-slider__track"></div>
          <div class="retro-slider__fill" :style="{ width: percent + '%' }"></div>
          <div class="retro-slider__thumb" :style="{ left: percent + '%' }"></div>
          <input
            class="retro-slider__native"
            type="range"
            :min="min"
            :max="max"
            :step="step"
            :value="value"
            :disabled="disabled"
            @input="onInput"
            @change="$emit('change', Number($event.target.value))"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HmSlider',
  props: {
    value: { type: Number, default: 50 },
    min: { type: Number, default: 0 },
    max: { type: Number, default: 100 },
    step: { type: Number, default: 1 },
    label: { type: String, default: '调节' },
    disabled: { type: Boolean, default: false }
  },
  computed: {
    percent() {
      const total = this.max - this.min
      if (total <= 0) return 0
      const clamped = Math.min(this.max, Math.max(this.min, this.value))
      return ((clamped - this.min) / total) * 100
    },
    displayValue() {
      return Number(this.value).toFixed(this.step < 1 ? 1 : 0)
    }
  },
  methods: {
    onInput(e) {
      this.$emit('input', Number(e.target.value))
    }
  }
}
</script>

<style scoped>
.retro-slider {
  width: 300px;
}

.retro-slider__frame {
  width: 100%;
  background: linear-gradient(160deg, #c8b89a, #7a6248);
  border-radius: 4px;
  padding: 4px;
  box-shadow:
    0 6px 0 #3a2e22,
    0 8px 12px rgba(0, 0, 0, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.25);
}

.retro-slider__inner {
  background: linear-gradient(180deg, #b8a080 0%, #6e5540 100%);
  border-radius: 3px;
  padding: 10px 12px 12px;
  box-shadow:
    inset 0 2px 4px rgba(0, 0, 0, 0.4),
    inset 0 -1px 2px rgba(255, 255, 255, 0.15);
}

.retro-slider__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.retro-slider__label,
.retro-slider__value {
  color: #f5e6cc;
  font-size: 12px;
  font-weight: bold;
  font-family: 'Courier New', monospace;
  letter-spacing: 1px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
}

.retro-slider__track-wrap {
  position: relative;
  height: 20px;
  display: flex;
  align-items: center;
}

.retro-slider__track {
  width: 100%;
  height: 8px;
  border-radius: 999px;
  background: linear-gradient(180deg, #4a392c, #2f241b);
  box-shadow:
    inset 0 2px 3px rgba(0, 0, 0, 0.55),
    0 1px 0 rgba(255, 255, 255, 0.12);
}

.retro-slider__fill {
  position: absolute;
  left: 0;
  height: 8px;
  border-radius: 999px;
  background: linear-gradient(90deg, #d8c09c, #f1ddb6);
  box-shadow: 0 0 8px rgba(241, 221, 182, 0.35);
  pointer-events: none;
}

.retro-slider__thumb {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #fff7e6, #d1b489 65%, #8f704d 100%);
  border: 1px solid #3b2d20;
  box-shadow:
    0 2px 5px rgba(0, 0, 0, 0.5),
    inset 0 1px 1px rgba(255, 255, 255, 0.5);
  pointer-events: none;
}

.retro-slider__native {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.retro-slider.disabled {
  opacity: 0.5;
}

.retro-slider.disabled .retro-slider__native {
  cursor: not-allowed;
}
</style>
