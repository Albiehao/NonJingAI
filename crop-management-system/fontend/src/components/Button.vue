<template>
  <button
    class="retro-btn"
    :class="[{ active: active, disabled: disabled }, `retro-btn--${size}`]"
    :type="type"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <div class="retro-btn__frame">
      <div class="retro-btn__inner">
        <span class="retro-btn__label">{{ label }}</span>
      </div>
    </div>
  </button>
</template>

<script>
export default {
  name: 'HmButton',
  props: {
    label: { type: String, default: '登录' },
    type: { type: String, default: 'submit' },
    active: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['md', 'nav'].includes(value)
    }
  }
}
</script>

<style scoped>
.retro-btn {
  border: none;
  background: none;
  padding: 0;
  cursor: pointer;
  outline: none;
}

.retro-btn__frame {
  width: 300px;
  height: 50px;
  background: linear-gradient(160deg, #9b8263, #5f4933);
  border-radius: 14px;
  padding: 4px;
  box-shadow:
    0 5px 0 #2b2118,
    0 7px 12px rgba(0,0,0,0.65),
    inset 0 1px 0 rgba(255,255,255,0.18);
  transition: all 0.08s ease;
  position: relative;
}

.retro-btn--nav .retro-btn__frame {
  width: 112px;
  height: 32px;
  border-radius: 10px;
  padding: 3px;
  box-shadow:
    0 3px 0 #2b2118,
    0 4px 8px rgba(0,0,0,0.55),
    inset 0 1px 0 rgba(255,255,255,0.16);
}

.retro-btn__inner {
  width: 100%;
  height: 100%;
  border-radius: 10px;
  background: linear-gradient(180deg, #947552 0%, #5a412d 100%);
  box-shadow:
    inset 0 2px 4px rgba(0,0,0,0.5),
    inset 0 -1px 2px rgba(255,255,255,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

/* 顶部高光 */
.retro-btn__inner::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 40%;
  background: linear-gradient(180deg, rgba(255,255,255,0.18), transparent);
  border-radius: 3px 3px 0 0;
}

.retro-btn__label {
  color: #f5e6cc;
  font-size: 12px;
  font-weight: bold;
  font-family: 'Courier New', monospace;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  text-shadow:
    0 1px 3px rgba(0,0,0,0.7),
    0 0 8px rgba(255,220,150,0.3);
  position: relative;
  z-index: 1;
}

.retro-btn--nav .retro-btn__label {
  font-size: 12px;
  letter-spacing: 1px;
}

/* 点击按下效果 */
.retro-btn:active:not(:disabled) .retro-btn__frame {
  box-shadow:
    0 2px 0 #3a2e22,
    0 3px 6px rgba(0,0,0,0.6),
    inset 0 1px 0 rgba(255,255,255,0.1);
  transform: translateY(3px);
}

/* 程序激活态 */
.retro-btn.active .retro-btn__frame {
  box-shadow:
    0 2px 0 #3a2e22,
    0 3px 6px rgba(0,0,0,0.6),
    inset 0 1px 0 rgba(255,255,255,0.1);
}

.retro-btn.active .retro-btn__inner {
  background: linear-gradient(180deg, #5a4535 0%, #8a6a50 100%);
  box-shadow:
    inset 0 3px 6px rgba(0,0,0,0.6),
    inset 0 -1px 2px rgba(255,255,255,0.1);
}

/* 激活时指示灯 */
.retro-btn.active .retro-btn__inner::after {
  content: '';
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ff6b35;
  box-shadow: 0 0 6px #ff6b35, 0 0 12px rgba(255,107,53,0.6);
}

.retro-btn.active .retro-btn__label {
  color: #ffe8b0;
  text-shadow:
    0 1px 3px rgba(0,0,0,0.8),
    0 0 10px rgba(255,220,100,0.6);
}

.retro-btn:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}
</style>
