<template>
  <header class="admin-topbar admin-card">
    <div class="topbar-left">
      <p class="topbar-kicker">ADMIN PANEL</p>
      <h2 class="topbar-title">{{ title }}</h2>
    </div>
    <div class="admin-user">
      <span class="avatar">{{ username.slice(0, 1).toUpperCase() }}</span>
      <div class="meta">
        <p class="name">{{ username }}</p>
        <p class="role">SYSTEM ADMIN</p>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AdminTopbar',
  props: {
    title: {
      type: String,
      default: 'Dashboard'
    },
    subtitle: {
      type: String,
      default: ''
    },
    stats: {
      type: Array,
      default: () => []
    },
    username: {
      type: String,
      default: 'Admin'
    }
  }
}
</script>

<style scoped>
.admin-topbar {
  padding: 12px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.topbar-kicker {
  font-size: 10px;
  letter-spacing: 1px;
  color: var(--admin-sub-text);
}

.topbar-title {
  margin-top: 4px;
  font-size: 16px;
  color: var(--admin-brand);
}

.admin-user {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding-left: 12px;
  border-left: 2px solid var(--admin-border);
}

.avatar {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--admin-border);
  color: var(--admin-brand);
  background: var(--admin-panel-2);
}

.name {
  font-size: 12px;
  color: var(--admin-text);
}

.role {
  margin-top: 2px;
  font-size: 10px;
  color: var(--admin-sub-text);
}

@media (max-width: 980px) {
  .meta {
    display: none;
  }
}
</style>
