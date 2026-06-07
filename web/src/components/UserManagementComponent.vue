<template>
  <div class="user-management">
    <!-- 头部区域 -->
    <div class="header-section">
      <div class="header-content">
        <h3 class="title">用户管理</h3>
        <p class="description">管理系统用户，请谨慎操作。删除用户后该用户将无法登录系统。</p>
      </div>
      <div class="header-actions">
        <a-segmented
          :value="viewMode"
          @change="(val) => (viewMode = val)"
          :options="[
            { label: '卡片', value: 'card' },
            { label: '列表', value: 'list' }
          ]"
          size="small"
        />
        <a-button type="primary" @click="showAddUserModal" class="add-btn">
          <template #icon><PlusOutlined /></template>
          添加用户
        </a-button>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="content-section">
      <a-spin :spinning="userManagement.loading">
        <div v-if="userManagement.error" class="error-message">
          <a-alert type="error" :message="userManagement.error" show-icon />
        </div>

        <!-- 卡片模式 -->
        <div v-show="viewMode === 'card'" class="cards-container">
          <div v-if="userManagement.users.length === 0" class="empty-state">
            <a-empty description="暂无用户数据" />
          </div>
          <div v-else class="user-cards-grid">
            <div v-for="user in userManagement.users" :key="user.id" class="user-card">
              <div class="card-header">
                <div class="user-info-main">
                  <div class="user-avatar">
                    <img
                      v-if="user.avatar"
                      :src="user.avatar"
                      :alt="user.username"
                      class="avatar-img"
                    />
                    <div v-else class="avatar-placeholder">
                      {{ user.username.charAt(0).toUpperCase() }}
                    </div>
                  </div>
                  <div class="user-info-content">
                    <div class="name-tag-row">
                      <h4 class="username">{{ user.username }}</h4>
                      <div
                        v-if="user.role === 'admin' || user.role === 'superadmin'"
                        class="role-dept-badge"
                      >
                        <span class="role-icon-wrapper" :class="getRoleClass(user.role)">
                          <UserLock v-if="user.role === 'superadmin'" :size="14" />
                          <UserStar v-else-if="user.role === 'admin'" :size="14" />
                          <User v-else :size="14" />
                        </span>
                      </div>
                    </div>
                    <div class="user-id-row">{{ user.username }}</div>
                  </div>
                </div>
              </div>

              <div class="card-content">
                <div class="info-item">
                  <span class="info-label">手机号:</span>
                  <span class="info-value phone-text">{{ user.phone_number || '-' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">创建时间:</span>
                  <span class="info-value time-text">{{ formatTime(user.created_at) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">最后登录:</span>
                  <span class="info-value time-text">{{ formatTime(user.last_login) }}</span>
                </div>
              </div>

              <div class="card-actions">
                <a-tooltip title="编辑用户">
                  <a-button
                    type="text"
                    size="small"
                    @click="showEditUserModal(user)"
                    class="action-btn"
                  >
                    <EditOutlined />
                    <span>编辑</span>
                  </a-button>
                </a-tooltip>
                <a-tooltip title="删除用户">
                  <a-button
                    type="text"
                    size="small"
                    danger
                    @click="confirmDeleteUser(user)"
                    :disabled="
                      user.id === userStore.userId ||
                      (user.role === 'superadmin' && userStore.userRole !== 'superadmin')
                    "
                    class="action-btn"
                  >
                    <DeleteOutlined />
                    <span>删除</span>
                  </a-button>
                </a-tooltip>
              </div>
            </div>
          </div>
        </div>

        <!-- 列表模式 -->
        <div v-show="viewMode === 'list'" class="list-container">
          <div v-if="userManagement.users.length === 0" class="empty-state">
            <a-empty description="暂无用户数据" />
          </div>
          <a-table
            v-else
            :dataSource="userManagement.users"
            :columns="tableColumns"
            :pagination="false"
            :loading="userManagement.loading"
            rowKey="id"
            size="middle"
            class="user-table"
          >
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'user'">
                <div class="table-user-cell">
                  <div class="table-avatar">
                    <img v-if="record.avatar" :src="record.avatar" :alt="record.username" class="avatar-img" />
                    <div v-else class="avatar-placeholder">{{ record.username.charAt(0).toUpperCase() }}</div>
                  </div>
                  <div class="table-user-info">
                    <span class="table-username">{{ record.username }}</span>
                  </div>
                </div>
              </template>
              <template v-if="column.key === 'role'">
                <span class="role-icon-wrapper" :class="getRoleClass(record.role)">
                  <UserLock v-if="record.role === 'superadmin'" :size="14" />
                  <UserStar v-else-if="record.role === 'admin'" :size="14" />
                  <User v-else :size="14" />
                </span>
                <span style="margin-left: 6px;">{{ record.role === 'superadmin' ? '超级管理员' : record.role === 'admin' ? '管理员' : '普通用户' }}</span>
              </template>
              <template v-if="column.key === 'phone'">
                <span class="table-phone">{{ record.phone_number || '-' }}</span>
              </template>
              <template v-if="column.key === 'created_at'">
                <span>{{ formatTime(record.created_at) }}</span>
              </template>
              <template v-if="column.key === 'last_login'">
                <span>{{ formatTime(record.last_login) }}</span>
              </template>
              <template v-if="column.key === 'actions'">
                <div class="table-actions">
                  <a-tooltip title="编辑用户">
                    <a-button type="link" size="small" @click="showEditUserModal(record)">
                      <EditOutlined />
                    </a-button>
                  </a-tooltip>
                  <a-tooltip title="删除用户">
                    <a-button
                      type="link"
                      size="small"
                      danger
                      @click="confirmDeleteUser(record)"
                      :disabled="
                        record.id === userStore.userId ||
                        (record.role === 'superadmin' && userStore.userRole !== 'superadmin')
                      "
                    >
                      <DeleteOutlined />
                    </a-button>
                  </a-tooltip>
                </div>
              </template>
            </template>
          </a-table>
        </div>
      </a-spin>
    </div>

    <!-- 用户表单模态框 -->
    <a-modal
      v-model:open="userManagement.modalVisible"
      :title="userManagement.modalTitle"
      @ok="handleUserFormSubmit"
      :confirmLoading="userManagement.loading"
      @cancel="userManagement.modalVisible = false"
      :maskClosable="false"
      width="480px"
      class="user-modal"
    >
      <a-form layout="vertical" class="user-form">
        <a-form-item label="用户名" required class="form-item">
          <a-input
            v-model:value="userManagement.form.username"
            placeholder="请输入用户名（2-20 个字符）"
            size="large"
            :maxlength="20"
          />
          <div v-if="userManagement.form.usernameError" class="error-text">
            {{ userManagement.form.usernameError }}
          </div>
        </a-form-item>

        <!-- 手机号字段 -->
        <a-form-item label="手机号" class="form-item">
          <a-input
            v-model:value="userManagement.form.phoneNumber"
            placeholder="请输入手机号（可选，可用于登录）"
            size="large"
            :maxlength="11"
          />
          <div v-if="userManagement.form.phoneError" class="error-text">
            {{ userManagement.form.phoneError }}
          </div>
        </a-form-item>

        <template v-if="userManagement.editMode">
          <div class="password-toggle">
            <a-checkbox v-model:checked="userManagement.displayPasswordFields">
              修改密码
            </a-checkbox>
          </div>
        </template>

        <template v-if="!userManagement.editMode || userManagement.displayPasswordFields">
          <a-form-item label="密码" required class="form-item">
            <a-input-password
              v-model:value="userManagement.form.password"
              placeholder="请输入密码"
              size="large"
            />
          </a-form-item>

          <a-form-item label="确认密码" required class="form-item">
            <a-input-password
              v-model:value="userManagement.form.confirmPassword"
              placeholder="请再次输入密码"
              size="large"
            />
          </a-form-item>
        </template>

        <a-form-item
          v-if="userManagement.editMode && userManagement.form.role === 'superadmin'"
          label="角色"
          class="form-item"
        >
          <a-input value="超级管理员" size="large" disabled />
          <div class="help-text">超级管理员账户无法修改角色</div>
        </a-form-item>
        <a-form-item v-else label="角色" class="form-item">
          <a-select v-model:value="userManagement.form.role" size="large">
            <a-select-option value="user">普通用户</a-select-option>
            <a-select-option value="admin" v-if="userStore.isSuperAdmin">管理员</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { reactive, onMounted, watch, ref } from 'vue'
import { notification, Modal } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'
import { DeleteOutlined, EditOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { User, UserLock, UserStar } from 'lucide-vue-next'
import { formatDateTime } from '@/utils/time'

const userStore = useUserStore()

// 用户管理相关状态
const userManagement = reactive({
  loading: false,
  users: [],
  error: null,
  modalVisible: false,
  modalTitle: '添加用户',
  editMode: false,
  editUserId: null,
  form: {
    username: '',
    phoneNumber: '',
    password: '',
    confirmPassword: '',
    role: 'user',
    usernameError: '',
    phoneError: ''
  },
  displayPasswordFields: true
})

// 视图模式
const viewMode = ref('card')

// 表格列定义
const tableColumns = [
  {
    title: '用户',
    key: 'user',
    dataIndex: 'username',
    width: 200
  },
  {
    title: '手机号',
    key: 'phone',
    dataIndex: 'phone_number',
    width: 140
  },
  {
    title: '角色',
    key: 'role',
    dataIndex: 'role',
    width: 120
  },
  {
    title: '创建时间',
    key: 'created_at',
    dataIndex: 'created_at',
    width: 180
  },
  {
    title: '最后登录',
    key: 'last_login',
    dataIndex: 'last_login',
    width: 180
  },
  {
    title: '操作',
    key: 'actions',
    width: 120
  }
]

// 验证手机号格式
const validatePhoneNumber = (phone) => {
  if (!phone) {
    return true
  }
  const phoneRegex = /^1[3-9]\d{9}$/
  return phoneRegex.test(phone)
}

// 监听密码字段显示状态变化
watch(
  () => userManagement.displayPasswordFields,
  (newVal) => {
    if (!newVal) {
      userManagement.form.password = ''
      userManagement.form.confirmPassword = ''
    }
  }
)

// 监听手机号输入变化
watch(
  () => userManagement.form.phoneNumber,
  (newPhone) => {
    userManagement.form.phoneError = ''

    if (newPhone && !validatePhoneNumber(newPhone)) {
      userManagement.form.phoneError = '请输入正确的手机号格式'
    }
  }
)

// 格式化时间显示
const formatTime = (timeStr) => formatDateTime(timeStr)

// 获取用户列表
const fetchUsers = async () => {
  try {
    userManagement.loading = true
    const users = await userStore.getUsers()
    userManagement.users = users
    userManagement.error = null
  } catch (error) {
    console.error('获取用户列表失败:', error)
    userManagement.error = '获取用户列表失败'
  } finally {
    userManagement.loading = false
  }
}

// 打开添加用户模态框
const showAddUserModal = () => {
  userManagement.modalTitle = '添加用户'
  userManagement.editMode = false
  userManagement.editUserId = null
  userManagement.form = {
    username: '',
    phoneNumber: '',
    password: '',
    confirmPassword: '',
    role: 'user',
    usernameError: '',
    phoneError: ''
  }
  userManagement.displayPasswordFields = true
  userManagement.modalVisible = true
}

// 打开编辑用户模态框
const showEditUserModal = (user) => {
  userManagement.modalTitle = '编辑用户'
  userManagement.editMode = true
  userManagement.editUserId = user.id
  userManagement.form = {
    username: user.username,
    phoneNumber: user.phone_number || '',
    password: '',
    confirmPassword: '',
    role: user.role,
    usernameError: '',
    phoneError: ''
  }
  userManagement.displayPasswordFields = false
  userManagement.modalVisible = true
}

// 处理用户表单提交
const handleUserFormSubmit = async () => {
  try {
    if (!userManagement.form.username.trim()) {
      notification.error({ message: '用户名不能为空' })
      return
    }

    if (
      userManagement.form.username.trim().length < 2 ||
      userManagement.form.username.trim().length > 20
    ) {
      notification.error({ message: '用户名长度必须在 2-20 个字符之间' })
      return
    }

    if (userManagement.form.phoneNumber && !validatePhoneNumber(userManagement.form.phoneNumber)) {
      notification.error({ message: '请输入正确的手机号格式' })
      return
    }

    if (userManagement.displayPasswordFields) {
      if (!userManagement.form.password) {
        notification.error({ message: '密码不能为空' })
        return
      }

      if (userManagement.form.password !== userManagement.form.confirmPassword) {
        notification.error({ message: '两次输入的密码不一致' })
        return
      }
    }

    userManagement.loading = true

    if (userManagement.editMode) {
      const updateData = {
        username: userManagement.form.username.trim(),
        role: userManagement.form.role
      }

      if (userManagement.form.phoneNumber) {
        updateData.phone_number = userManagement.form.phoneNumber
      }

      if (userManagement.displayPasswordFields && userManagement.form.password) {
        updateData.password = userManagement.form.password
      }

      await userStore.updateUser(userManagement.editUserId, updateData)
      notification.success({ message: '用户更新成功' })
    } else {
      const createData = {
        username: userManagement.form.username.trim(),
        password: userManagement.form.password,
        role: userManagement.form.role
      }

      if (userManagement.form.phoneNumber) {
        createData.phone_number = userManagement.form.phoneNumber
      }

      await userStore.createUser(createData)
      notification.success({ message: '用户创建成功' })
    }

    await fetchUsers()
    userManagement.modalVisible = false
  } catch (error) {
    console.error('用户操作失败:', error)
    notification.error({
      message: '操作失败',
      description: error.message || '请稍后重试'
    })
  } finally {
    userManagement.loading = false
  }
}

// 删除用户
const confirmDeleteUser = (user) => {
  if (user.id === userStore.userId) {
    notification.error({ message: '不能删除自己的账户' })
    return
  }

  Modal.confirm({
    title: '确认删除用户',
    content: `确定要删除用户 "${user.username}" 吗？此操作不可撤销。`,
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    async onOk() {
      try {
        userManagement.loading = true
        await userStore.deleteUser(user.id)
        notification.success({ message: '用户删除成功' })
        await fetchUsers()
      } catch (error) {
        console.error('删除用户失败:', error)
        notification.error({
          message: '删除失败',
          description: error.message || '请稍后重试'
        })
      } finally {
        userManagement.loading = false
      }
    }
  })
}

const getRoleClass = (role) => {
  switch (role) {
    case 'superadmin':
      return 'role-superadmin'
    case 'admin':
      return 'role-admin'
    case 'user':
      return 'role-user'
    default:
      return 'role-default'
  }
}

onMounted(async () => {
  await fetchUsers()
})
</script>

<style lang="less" scoped>
.user-management {
  margin-top: 12px;
  min-height: 50vh;

  .header-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;

    .header-content {
      flex: 1;

      .description {
        font-size: 14px;
        color: var(--gray-600);
        margin: 0;
        line-height: 1.4;
        margin-bottom: 16px;
      }
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }
  }

  .content-section {
    overflow: hidden;

    .error-message {
      padding: 16px 24px;
    }

    .cards-container {
      .empty-state {
        padding: 60px 20px;
        text-align: center;
      }

      .user-cards-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;

        .user-card {
          background: var(--gray-0);
          border: 1px solid var(--gray-150);
          border-radius: 8px;
          padding: 12px;
          padding-bottom: 6px;

          transition: all 0.2s ease;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);

          &:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            border-color: var(--gray-200);
          }

          .card-header {
            margin-bottom: 10px;

            .user-info-main {
              display: flex;
              gap: 12px;
              align-items: center;

              .user-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: var(--gray-50);
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                flex-shrink: 0;

                .avatar-img {
                  width: 100%;
                  height: 100%;
                  object-fit: cover;
                }

                .avatar-placeholder {
                  color: var(--gray-600);
                  font-weight: 500;
                  font-size: 14px;
                }
              }

              .user-info-content {
                flex: 1;
                min-width: 0;

                .name-tag-row {
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  gap: 8px;
                  margin-bottom: 2px;
                  flex-wrap: wrap;

                  .username {
                    margin: 0;
                    font-size: 15px;
                    font-weight: 600;
                    color: var(--gray-900);
                    line-height: 1.2;
                    flex-shrink: 0;
                  }

                  .role-dept-badge {
                    display: inline-flex;
                    align-items: center;
                    gap: 4px;
                    padding: 2px 8px 2px 4px;
                    background: var(--gray-50);
                    border-radius: 4px;

                    .role-icon-wrapper {
                      display: flex;
                      align-items: center;
                      justify-content: center;
                      width: 16px;
                      height: 16px;

                      &.role-superadmin {
                        color: var(--color-error-700);
                      }
                      &.role-admin {
                        color: var(--color-info-700);
                      }
                      &.role-user {
                        color: var(--color-success-700);
                      }
                    }
                  }
                }

                .user-id-row {
                  font-size: 12px;
                  color: var(--gray-500);
                  font-family: 'Monaco', 'Consolas', monospace;
                  line-height: 1.2;
                }
              }
            }
          }

          .card-content {
            .info-item {
              display: flex;
              justify-content: space-between;
              align-items: center;
              padding: 2px 0;
              border-bottom: 1px solid var(--gray-25);

              &:last-child {
                border-bottom: none;
              }

              .info-label {
                font-size: 12px;
                color: var(--gray-600);
                font-weight: 500;
                min-width: 70px;
              }

              .info-value {
                font-size: 12px;
                color: var(--gray-900);
                text-align: right;
                flex: 1;

                &.time-text {
                  color: var(--gray-700);
                }

                &.phone-text {
                  font-family: 'Monaco', 'Consolas', monospace;
                }
              }
            }
          }

          .card-actions {
            display: flex;
            justify-content: flex-end;
            gap: 6px;
            padding-top: 6px;
            border-top: 1px solid var(--gray-25);

            .action-btn {
              display: flex;
              align-items: center;
              gap: 4px;
              padding: 4px 8px;
              border-radius: 6px;
              transition: all 0.2s ease;
              font-size: 12px;

              span {
                font-size: 12px;
              }

              &:hover {
                background: var(--gray-25);
              }

              &.ant-btn-dangerous:hover {
                background: var(--gray-25);
                border-color: var(--color-error-500);
                color: var(--color-error-500);
              }
            }
          }
        }
      }
    }

    .list-container {
      .user-table {
        :deep(.ant-table-thead > tr > th) {
          background: var(--gray-50);
          color: var(--gray-700);
          font-weight: 600;
          font-size: 13px;
          border-bottom: 1px solid var(--gray-150);
        }

        :deep(.ant-table-tbody > tr > td) {
          border-bottom: 1px solid var(--gray-50);
        }

        :deep(.ant-table-tbody > tr:hover > td) {
          background: var(--gray-25);
        }

        .table-user-cell {
          display: flex;
          align-items: center;
          gap: 10px;

          .table-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--gray-50);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            flex-shrink: 0;

            .avatar-img {
              width: 100%;
              height: 100%;
              object-fit: cover;
            }

            .avatar-placeholder {
              color: var(--gray-600);
              font-weight: 500;
              font-size: 13px;
            }
          }

          .table-user-info {
            display: flex;
            flex-direction: column;
            gap: 1px;

            .table-username {
              font-weight: 600;
              font-size: 14px;
              color: var(--gray-900);
              line-height: 1.3;
            }

            .table-user-id {
              font-size: 12px;
              color: var(--gray-500);
              font-family: 'Monaco', 'Consolas', monospace;
              line-height: 1.3;
            }
          }
        }

        .table-phone {
          font-size: 13px;
          font-family: 'Monaco', 'Consolas', monospace;
          color: var(--gray-700);
        }

        .table-actions {
          display: flex;
          gap: 4px;

          :deep(.ant-btn-link) {
            padding: 4px 6px;
            color: var(--gray-600);
            height: auto;
            border-radius: 4px;

            &:hover {
              color: var(--main-700);
              background: var(--gray-50);
            }

            &[danger]:hover {
              color: var(--color-error-500);
              background: var(--error-10);
            }
          }
        }
      }
    }
  }

  .time-text {
    font-size: 13px;
    color: var(--gray-700);
  }

  .phone-text,
  .user-id-text {
    font-size: 13px;
    color: var(--gray-900);
    font-family: 'Monaco', 'Consolas', monospace;
  }
}

.user-modal {
  :deep(.ant-modal-header) {
    padding: 20px 24px;
    border-bottom: 1px solid var(--gray-150);

    .ant-modal-title {
      font-size: 16px;
      font-weight: 600;
      color: var(--gray-900);
    }
  }

  :deep(.ant-modal-body) {
    padding: 24px;
  }

  .user-form {
    .form-item {
      margin-bottom: 20px;

      :deep(.ant-form-item-label) {
        padding-bottom: 4px;

        label {
          font-weight: 500;
          color: var(--gray-900);
        }
      }
    }

    .error-text {
      color: var(--color-error-500);
      font-size: 12px;
      margin-top: 4px;
      line-height: 1.3;
    }

    .help-text {
      color: var(--gray-600);
      font-size: 12px;
      margin-top: 4px;
      line-height: 1.3;
    }

    .password-toggle {
      margin-bottom: 16px;

      :deep(.ant-checkbox-wrapper) {
        font-weight: 500;
        color: var(--gray-600);
      }
    }
  }
}
</style>
