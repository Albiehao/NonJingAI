<template>
  <div class="settings-view">
    <div class="settings-header">
      <h2>系统设置</h2>
    </div>
    <div class="settings-body">
      <!-- Tab Navigation -->
      <div class="settings-tabs">
        <div
          class="tab-item"
          :class="{ active: activeTab === 'base' }"
          @click="activeTab = 'base'"
          v-if="userStore.isSuperAdmin"
        >
          <SettingOutlined class="tab-icon" />
          <span>基本设置</span>
        </div>
        <div
          class="tab-item"
          :class="{ active: activeTab === 'model' }"
          @click="activeTab = 'model'"
          v-if="userStore.isSuperAdmin"
        >
          <CodeOutlined class="tab-icon" />
          <span>模型配置</span>
        </div>
        <div
          class="tab-item"
          :class="{ active: activeTab === 'user' }"
          @click="activeTab = 'user'"
          v-if="userStore.isAdmin"
        >
          <UserOutlined class="tab-icon" />
          <span>用户管理</span>
        </div>
        <div
          class="tab-item"
          :class="{ active: activeTab === 'email' }"
          @click="activeTab = 'email'"
          v-if="userStore.isSuperAdmin"
        >
          <MailOutlined class="tab-icon" />
          <span>邮件设置</span>
        </div>
      </div>

      <!-- Content -->
      <div class="settings-content">
        <div v-show="activeTab === 'base'" v-if="userStore.isSuperAdmin">
          <BasicSettingsSection />
        </div>
        <div v-show="activeTab === 'model'" v-if="userStore.isSuperAdmin">
          <ModelProvidersComponent />
        </div>
        <div v-show="activeTab === 'user'" v-if="userStore.isAdmin">
          <UserManagementComponent />
        </div>
        <div v-show="activeTab === 'email'" v-if="userStore.isSuperAdmin">
          <EmailSettingsSection />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { SettingOutlined, CodeOutlined, UserOutlined, MailOutlined } from '@ant-design/icons-vue'
import BasicSettingsSection from '@/components/BasicSettingsSection.vue'
import ModelProvidersComponent from '@/components/ModelProvidersComponent.vue'
import UserManagementComponent from '@/components/UserManagementComponent.vue'
import EmailSettingsSection from '@/components/EmailSettingsSection.vue'

const userStore = useUserStore()
const activeTab = ref('base')
</script>

<style lang="less" scoped>
.settings-view {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;

  .settings-header {
    flex-shrink: 0;
    padding: 16px 24px 0;

    h2 {
      font-size: 20px;
      font-weight: 600;
      color: var(--gray-900);
      margin: 0;
    }
  }

  .settings-body {
    flex: 1;
    display: flex;
    padding: 16px 24px;
    overflow: hidden;
    gap: 24px;

    .settings-tabs {
      width: 140px;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      gap: 4px;
      padding-top: 4px;

      .tab-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 14px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 15px;
        color: var(--gray-700);
        transition: all 0.15s;

        .tab-icon {
          font-size: 15px;
        }

        &:hover {
          background: var(--gray-50);
        }

        &.active {
          background: var(--gray-100);
          color: var(--main-700);
          font-weight: 500;
        }
      }
    }

    .settings-content {
      flex: 1;
      overflow-y: auto;
      min-width: 0;
    }
  }
}
</style>
