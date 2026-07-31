<template>
  <aside class="admin-sidebar admin-card" :class="{ open: mobileOpen }">
    <button class="mobile-trigger admin-btn" type="button" @click="$emit('toggle-mobile')">
      {{ mobileOpen ? '鏀惰捣鑿滃崟' : '灞曞紑鑿滃崟' }}
    </button>

    <div class="brand">
      <span class="brand-mark">HEXIN</span>
      <p class="brand-cn">农业后台管理台</p>
      <p class="brand-en">Data, Products and Field Operations</p>
    </div>

    <div class="nav-meta">
      <span class="nav-dot"></span>
      <span>Modules</span>
    </div>

    <ul class="menu">
      <li
        v-for="item in menus"
        :key="item.key"
        :class="{ active: currentMenu === item.key }"
        @click="$emit('select', item.key)"
      >
        <span class="menu-index">{{ item.label.slice(0, 2) }}</span>
        <span class="menu-label">{{ item.label }}</span>
      </li>
    </ul>

    <div class="sidebar-foot">
      <p class="foot-title">Workspace Status</p>
      <p class="foot-copy">统一管理用户、作物、商品和关联关系。</p>
    </div>
  </aside>
</template>

<script>
export default {
  name: 'AdminSidebar',
  props: {
    menus: {
      type: Array,
      default: () => []
    },
    currentMenu: {
      type: String,
      default: 'dashboard'
    },
    mobileOpen: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.admin-sidebar {
  padding: 18px;
  align-self: stretch;
  height: 100%;
  min-height: 0;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.mobile-trigger {
  display: none;
  width: 100%;
  margin-bottom: 12px;
}

.brand {
  padding: 18px;
  border: 1px solid var(--admin-border-soft, var(--admin-border));
  background:
    radial-gradient(circle at top right, rgba(255, 207, 106, 0.18), transparent 28%),
    var(--admin-panel-2);
}

.brand-mark {
  display: inline-flex;
  padding: 6px 10px;
  background: rgba(255, 207, 106, 0.14);
  color: var(--admin-accent);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.14em;
}

.brand-cn {
  margin-top: 14px;
  color: var(--admin-brand);
  font-size: 24px;
  font-weight: 700;
  line-height: 1.25;
}

.brand-en {
  margin-top: 10px;
  color: var(--admin-sub-text);
  font-size: 12px;
  line-height: 1.6;
}

.nav-meta {
  margin-top: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--admin-sub-text);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.nav-dot {
  width: 8px;
  height: 8px;
  background: var(--admin-success);
  box-shadow: 0 0 12px rgba(103, 212, 162, 0.4);
}

.menu {
  margin-top: 14px;
  display: grid;
  gap: 10px;
}

.menu li {
  padding: 14px 14px 14px 12px;
  border: 1px solid transparent;
  background: rgba(255, 255, 255, 0.03);
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--admin-text);
  cursor: pointer;
  transition: transform 0.18s ease, background 0.2s ease, border-color 0.2s ease;
}

.menu li:hover {
  transform: translateX(2px);
  border-color: var(--admin-border-soft, var(--admin-border));
  background: rgba(255, 255, 255, 0.06);
}

.menu li.active {
  border-color: rgba(255, 207, 106, 0.22);
  background: linear-gradient(135deg, rgba(255, 207, 106, 0.18), rgba(255, 207, 106, 0.05));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.menu-index {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--admin-panel-3, var(--admin-panel-2));
  color: var(--admin-accent);
  font-size: 12px;
  font-weight: 700;
}

.menu-label {
  font-size: 14px;
  font-weight: 600;
}

.sidebar-foot {
  margin-top: auto;
  padding: 16px;
  border: 1px solid var(--admin-border-soft, var(--admin-border));
  background: rgba(255, 255, 255, 0.03);
}

.foot-title {
  color: var(--admin-brand);
  font-size: 12px;
  font-weight: 700;
}

.foot-copy {
  margin-top: 8px;
  color: var(--admin-sub-text);
  font-size: 12px;
  line-height: 1.7;
}

@media (max-width: 980px) {
  .admin-sidebar {
    height: auto;
    padding: 14px;
  }

  .mobile-trigger {
    display: block;
  }

  .menu,
  .nav-meta,
  .sidebar-foot {
    display: none;
  }

  .admin-sidebar.open .menu,
  .admin-sidebar.open .nav-meta,
  .admin-sidebar.open .sidebar-foot {
    display: grid;
  }

  .admin-sidebar.open .nav-meta {
    display: flex;
  }
}
</style>

