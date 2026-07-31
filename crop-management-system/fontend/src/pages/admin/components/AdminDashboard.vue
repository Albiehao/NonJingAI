<template>
  <div class="dashboard-shell">
    <section class="admin-panel clock-panel" aria-label="System Clock">
      <div class="clock-panel-top">
        <div>
          <p class="clock-kicker">LIVE STATUS</p>
          <h3 class="admin-panel-title">系统时间</h3>
          <p class="clock-caption">与当前设备本地时间同步，便于判断后台操作节奏。</p>
        </div>
        <div class="clock-live">
          <span class="clock-live-dot"></span>
          <span>实时刷新</span>
        </div>
      </div>

      <div class="clock-face">
        <div
          v-for="(segment, idx) in clockSegments"
          :key="`${segment}-${idx}`"
          class="clock-segment"
        >
          <span class="clock-segment-label">{{ segmentLabels[idx] }}</span>
          <strong class="clock-segment-value">{{ segment }}</strong>
        </div>
      </div>

      <div class="clock-meta">
        <div class="clock-meta-card">
          <span class="clock-meta-label">日期</span>
          <strong class="clock-meta-value">{{ clockDate }}</strong>
        </div>
        <div class="clock-meta-card">
          <span class="clock-meta-label">星期</span>
          <strong class="clock-meta-value">{{ clockWeekday }}</strong>
        </div>
        <div class="clock-meta-card">
          <span class="clock-meta-label">时段</span>
          <strong class="clock-meta-value">{{ periodLabel }}</strong>
        </div>
        <div class="clock-meta-card">
          <span class="clock-meta-label">时区</span>
          <strong class="clock-meta-value">{{ clockTimezone }}</strong>
        </div>
      </div>
    </section>

    <section class="admin-panel merged-overview">
      <div class="merged-main">
        <p class="merged-kicker">CONTROL CENTER</p>
        <h3 class="admin-panel-title">后台运行概览</h3>
        <p class="merged-desc">
          当前共管理 {{ usersCount }} 个用户、{{ productsCount }} 个商品与 {{ cropsCount }} 个作物条目，
          可重点关注商品沉淀和用户作物关联的完整度。
        </p>
      </div>
      <div class="merged-user">
        <span class="user-role">SYSTEM ADMIN</span>
      </div>
    </section>

    <section class="admin-panel">
      <div class="admin-panel-head">
        <h3 class="admin-panel-title">核心数据</h3>
      </div>
      <div class="card-grid">
        <article class="stat-card admin-card">
          <p class="stat-label">用户</p>
          <p class="stat-value">{{ usersCount }}</p>
        </article>
        <article class="stat-card admin-card">
          <p class="stat-label">商品</p>
          <p class="stat-value">{{ productsCount }}</p>
        </article>
        <article class="stat-card admin-card">
          <p class="stat-label">作物</p>
          <p class="stat-value">{{ cropsCount }}</p>
        </article>
        <article class="stat-card admin-card">
          <p class="stat-label">关联</p>
          <p class="stat-value">{{ totalStock }}</p>
        </article>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  props: {
    usersCount: { type: Number, default: 0 },
    categoriesCount: { type: Number, default: 0 },
    productsCount: { type: Number, default: 0 },
    totalStock: { type: Number, default: 0 },
    cropsCount: { type: Number, default: 0 }
  },
  data() {
    return {
      timer: null,
      clockTime: '',
      clockDate: '',
      clockWeekday: '',
      clockTimezone: 'Local Time',
      segmentLabels: ['小时', '分钟', '秒']
    }
  },
  computed: {
    clockSegments() {
      return this.clockTime.split(':')
    },
    periodLabel() {
      const hour = Number(this.clockSegments[0] || 0)
      if (hour < 6) return '凌晨'
      if (hour < 12) return '上午'
      if (hour < 14) return '中午'
      if (hour < 18) return '下午'
      return '晚上'
    }
  },
  created() {
    this.clockTimezone = this.resolveTimezone()
    this.updateClock()
    this.timer = setInterval(this.updateClock, 1000)
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  methods: {
    resolveTimezone() {
      try {
        const { timeZone } = Intl.DateTimeFormat().resolvedOptions()
        return timeZone || 'Local Time'
      } catch (e) {
        return 'Local Time'
      }
    },
    updateClock() {
      const now = new Date()
      const pad = n => String(n).padStart(2, '0')
      const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
      this.clockTime = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`
      this.clockDate = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`
      this.clockWeekday = weekdays[now.getDay()]
    }
  }
}
</script>

<style scoped>
.dashboard-shell {
  display: grid;
  gap: 14px;
}

.clock-kicker,
.merged-kicker {
  font-size: 11px;
  color: var(--admin-sub-text);
  letter-spacing: 1.6px;
}

.clock-panel {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at top right, rgba(255, 207, 106, 0.18), transparent 28%),
    radial-gradient(circle at bottom left, rgba(103, 212, 162, 0.14), transparent 24%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.05), transparent 48%),
    var(--admin-panel);
}

.clock-panel::after {
  content: '';
  position: absolute;
  inset: auto -40px -70px auto;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  border: 1px solid rgba(255, 207, 106, 0.12);
  box-shadow:
    0 0 0 22px rgba(255, 207, 106, 0.05),
    0 0 0 48px rgba(255, 207, 106, 0.03);
  pointer-events: none;
}

.clock-panel-top {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.clock-caption {
  margin-top: 8px;
  max-width: 560px;
  color: var(--admin-sub-text);
  font-size: 13px;
  line-height: 1.7;
}

.clock-live {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border: 1px solid rgba(255, 207, 106, 0.18);
  background: rgba(18, 25, 36, 0.54);
  color: var(--admin-brand);
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.clock-live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--admin-success);
  box-shadow: 0 0 0 5px rgba(103, 212, 162, 0.16);
  animation: pulse-dot 1.8s ease-in-out infinite;
}

.clock-face {
  position: relative;
  z-index: 1;
  margin-top: 22px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.clock-segment {
  position: relative;
  padding: 18px 18px 16px;
  border: 1px solid rgba(255, 207, 106, 0.16);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.06), transparent 26%),
    rgba(18, 24, 34, 0.62);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.05),
    0 16px 26px rgba(7, 11, 18, 0.18);
}

.clock-segment-label {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.14em;
  color: var(--admin-sub-text);
  text-transform: uppercase;
}

.clock-segment-value {
  display: block;
  margin-top: 12px;
  font-size: clamp(34px, 6vw, 56px);
  line-height: 1;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: var(--admin-brand);
}

.clock-meta {
  position: relative;
  z-index: 1;
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.clock-meta-card {
  padding: 12px 14px;
  border-top: 1px solid var(--admin-border-soft);
  background: rgba(255, 255, 255, 0.03);
}

.clock-meta-label {
  display: block;
  font-size: 11px;
  letter-spacing: 0.08em;
  color: var(--admin-sub-text);
}

.clock-meta-value {
  display: block;
  margin-top: 8px;
  font-size: 14px;
  color: var(--admin-text);
  word-break: break-word;
}

.merged-overview {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.merged-desc {
  margin-top: 10px;
  max-width: 760px;
  color: var(--admin-sub-text);
  font-size: 13px;
  line-height: 1.8;
}

.merged-user {
  min-width: 120px;
  padding-left: 14px;
  border-left: 2px solid var(--admin-border);
}

.user-role {
  display: inline-block;
  color: var(--admin-brand);
  font-size: 12px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.stat-card {
  padding: 16px;
  background: var(--admin-panel-2);
}

.stat-label {
  font-size: 12px;
  color: var(--admin-sub-text);
}

.stat-value {
  margin-top: 12px;
  font-size: 34px;
  font-weight: 700;
  line-height: 1;
  color: var(--admin-accent);
}

@keyframes pulse-dot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.82); opacity: 0.7; }
}

.admin-page.light-mode .clock-panel {
  background:
    radial-gradient(circle at top right, rgba(191, 122, 39, 0.14), transparent 26%),
    radial-gradient(circle at bottom left, rgba(47, 136, 96, 0.12), transparent 24%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.38), transparent 48%),
    var(--admin-panel);
}

.admin-page.light-mode .clock-live,
.admin-page.light-mode .clock-segment {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.56), transparent 28%),
    rgba(255, 250, 242, 0.72);
}

.admin-page.light-mode .clock-live {
  border-color: rgba(157, 98, 31, 0.2);
}

.admin-page.light-mode .clock-live-dot {
  box-shadow: 0 0 0 5px rgba(47, 136, 96, 0.12);
}

.admin-page.light-mode .clock-segment {
  border-color: rgba(157, 98, 31, 0.18);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    0 14px 24px rgba(164, 132, 98, 0.12);
}

.admin-page.light-mode .clock-segment-value {
  color: var(--admin-accent);
}

.admin-page.light-mode .clock-meta-card {
  background: rgba(255, 255, 255, 0.42);
}

@media (max-width: 1100px) {
  .clock-meta {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .card-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .clock-panel-top,
  .merged-overview {
    flex-direction: column;
  }

  .clock-face,
  .clock-meta {
    grid-template-columns: 1fr;
  }

  .merged-user {
    min-width: 0;
    padding-left: 0;
    border-left: none;
    border-top: 2px solid var(--admin-border);
    padding-top: 12px;
  }

  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
