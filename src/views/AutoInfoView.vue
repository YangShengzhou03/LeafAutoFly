<template>
  <div class="auto-info-container">
    <div class="page-header">
      <h1>LeafAuto Info</h1>
    </div>

    <!-- 通知提示区域 -->
    <div class="notification-container" ref="notificationContainer"></div>

    <!-- 任务创建卡片 -->
    <div class="task-creation-card animate-fade-in">
      <div class="card-header">
        <h2 class="card-title">
          <span class="plus-icon"></span>创建新任务
        </h2>
        <p class="card-subtitle">设置自动发送的信息内容、接收者和发送时间</p>
      </div>
      <div class="card-body">
        <el-form ref="taskForm" :model="formData" :rules="rules" label-width="100px">
          <div class="form-grid">
            <el-form-item label="接收者" prop="recipient" required>
              <div class="recipient-input-wrapper">
                <el-input
                  v-model="formData.recipient"
                  placeholder="输入接收者信息"
                  clearable
                >
                  <template #suffix>
                    <span class="contact-icon"></span>
                  </template>
                </el-input>
              </div>
              <div class="field-hint">多个接收者用逗号分隔</div>
            </el-form-item>

            <el-form-item label="发送时间" prop="sendTime" required>
              <el-date-picker
                v-model="formData.sendTime"
                type="datetime"
                placeholder="选择发送时间"
                value-format="YYYY-MM-DDTHH:mm"
                :default-value="defaultDateTime"
              ></el-date-picker>
            </el-form-item>

            <el-form-item label="重复选项">
              <div class="repeat-dropdown">
                <el-button
                  type="default"
                  class="repeat-btn"
                  @click="toggleRepeatOptions"
                >
                  {{ repeatBtnText }} <span class="dropdown-icon"></span>
                </el-button>
                <div
                  class="repeat-options"
                  v-show="showRepeatOptions"
                >
                  <div
                    class="repeat-option"
                    v-for="option in repeatOptions"
                    :key="option.value"
                    @click="selectRepeatOption(option)"
                  >
                    {{ option.label }}
                  </div>
                  <div class="custom-days" v-show="formData.repeatType === 'custom'
">
                    <p class="form-text mb-2">选择重复日期：</p>
                    <div class="day-selector">
                      <label v-for="day in daysOfWeek" :key="day.value">
                        <el-checkbox
                          v-model="formData.repeatDays"
                          :label="day.value"
                        ></el-checkbox>
                        <span>{{ day.label }}</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </el-form-item>

            <el-form-item label="信息内容" prop="messageContent" required class="full-width">
              <el-input
                v-model="formData.messageContent"
                type="textarea"
                placeholder="输入信息内容"
                :rows="4"
                @input="updateCharCount"
              ></el-input>
              <div class="char-count">{{ charCount }}/500</div>
            </el-form-item>
          </div>

          <div class="form-actions">
            <el-button type="default" @click="resetForm">重置</el-button>
            <span class="actions-separator"></span>
            <el-button type="primary" @click="submitForm">
              <span class="play-icon"></span> 创建任务
            </el-button>
          </div>
        </el-form>
      </div>
    </div>

    <!-- 任务列表区域 -->
    <div class="task-list-container">
      <div class="task-list-header">
        <div class="header-content">
          <h2>任务列表</h2>
          <p class="list-description">当前共有 {{ tasks.length }} 个任务</p>
        </div>
        <div class="task-list-actions">
          <el-button type="primary" plain :disabled="tasks.length === 0">导入</el-button>
          <el-button type="primary" plain :disabled="tasks.length === 0">导出</el-button>
          <el-button type="primary" :disabled="tasks.length === 0">开始执行</el-button>
        </div>
      </div>

      <ul class="task-list" v-if="tasks.length > 0">
        <li
          v-for="task in sortedTasks"
          :key="task.id"
          class="task-item task-transition"
          :data-task-id="task.id"
        >
          <div class="task-content">
            <h3 class="task-recipient">接收者: {{ task.recipient }}</h3>
            <p class="task-message">内容: {{ task.messageContent }}</p>
            <div class="task-meta">
              <span class="task-time"><i class="fa fa-clock-o"></i> {{ formatDateTime(task.sendTime) }}</span>
              <span class="task-repeat"><i class="fa fa-refresh"></i> {{ getRepeatText(task.repeatType, task.repeatDays) }}</span>
              <span :class="['task-status', task.status]">{{ task.status === 'pending' ? '待执行' : '已完成' }}</span>
            </div>
          </div>
          <div class="task-actions">
            <el-button
              type="danger"
              size="small"
              @click="deleteTask(task.id)"
              icon="Delete"
            >
              删除
            </el-button>
          </div>
        </li>
      </ul>

      <div class="empty-task-state" v-else>
        <div class="empty-state-image animate-fade-in">
          <img src="../assets/images/empty-tasks.svg" alt="暂无任务" class="empty-state-icon">
        </div>
        <h3 class="empty-state-title">暂无任务</h3>
        <p class="empty-state-description">点击上方的"创建新任务"按钮，开始创建您的第一个自动信息任务</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'

// 表单数据
const formData = reactive({
  recipient: '',
  sendTime: '',
  repeatType: 'none',
  repeatDays: [],
  messageContent: ''
})

// 表单验证规则
const rules = {
  recipient: [
    { required: true, message: '请输入接收者', trigger: 'blur' },
    { validator: validateRecipient, trigger: 'blur' }
  ],
  sendTime: [
    { required: true, message: '请选择发送时间', trigger: 'change' }
  ],
  messageContent: [
    { required: true, message: '请输入消息内容', trigger: 'blur' },
    { max: 500, message: '消息内容不能超过500个字符', trigger: 'input' }
  ]
}

// 验证接收者格式
function validateRecipient(rule, value, callback) {
  if (!value.trim()) {
    callback(new Error('请输入接收者'))
    return
  }
  // 简单验证，实际应用中可能需要更复杂的验证
  callback()
}

// 任务列表数据
const tasks = ref([])

// 重复选项数据
const repeatOptions = [
  { label: '不重复', value: 'none' },
  { label: '每天', value: 'daily' },
  { label: '法定工作日', value: 'workday' },
  { label: '法定节假日', value: 'holiday' },
  { label: '自定义', value: 'custom' }
]

// 星期几数据
const daysOfWeek = [
  { label: '周一', value: '1' },
  { label: '周二', value: '2' },
  { label: '周三', value: '3' },
  { label: '周四', value: '4' },
  { label: '周五', value: '5' },
  { label: '周六', value: '6' },
  { label: '周日', value: '0' }
]

// 重复按钮文本
const repeatBtnText = computed(() => {
  const option = repeatOptions.find(opt => opt.value === formData.repeatType)
  return option ? option.label : '不重复'
})

// 显示重复选项下拉菜单
const showRepeatOptions = ref(false)

// 字符计数
const charCount = ref(0)

// 默认日期时间
const defaultDateTime = computed(() => {
  const now = new Date()
  now.setMinutes(now.getMinutes() + 30)
  return now
})

// 排序后的任务列表
const sortedTasks = computed(() => {
  return [...tasks.value].sort((a, b) => new Date(a.sendTime) - new Date(b.sendTime))
})

// 切换重复选项下拉菜单
function toggleRepeatOptions() {
  showRepeatOptions.value = !showRepeatOptions.value
}

// 选择重复选项
function selectRepeatOption(option) {
  formData.repeatType = option.value
  showRepeatOptions.value = false
}

// 更新字符计数
function updateCharCount() {
  charCount.value = formData.messageContent.length
  if (charCount.value > 500) {
    formData.messageContent = formData.messageContent.substring(0, 500)
    charCount.value = 500
  }
}

// 重置表单
function resetForm() {
  formData.recipient = ''
  formData.sendTime = ''
  formData.repeatType = 'none'
  formData.repeatDays = []
  formData.messageContent = ''
  charCount.value = 0
}

// 提交表单
function submitForm() {
  const taskForm = document.querySelector('#taskForm')
  if (taskForm) {
    if (!formData.recipient.trim()) {
      ElMessage.error('请输入接收者')
      return
    }
    if (!formData.sendTime) {
      ElMessage.error('请选择发送时间')
      return
    }
    if (!formData.messageContent.trim()) {
      ElMessage.error('请输入消息内容')
      return
    }
    if (formData.repeatType === 'custom' && formData.repeatDays.length === 0) {
      ElMessage.error('请至少选择一个重复日期')
      return
    }

    // 模拟API请求
    setTimeout(() => {
      const newTask = {
        id: Date.now(),
        recipient: formData.recipient,
        sendTime: formData.sendTime,
        repeatType: formData.repeatType,
        repeatDays: formData.repeatDays,
        messageContent: formData.messageContent,
        status: 'pending'
      }
      tasks.value.push(newTask)
      ElMessage.success('任务创建成功')
      resetForm()
    }, 500)
  }
}

// 删除任务
function deleteTask(taskId) {
  ElMessage.confirm('确定要删除这个任务吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    tasks.value = tasks.value.filter(task => task.id !== taskId)
    ElMessage.success('任务删除成功')
  }).catch(() => {
    // 用户取消删除
  })
}

// 格式化日期时间
function formatDateTime(dateString) {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${padZero(date.getMonth() + 1)}-${padZero(date.getDate())} ${padZero(date.getHours())}:${padZero(date.getMinutes())}`
}

// 补零函数
function padZero(num) {
  return num < 10 ? '0' + num : num
}

// 获取重复文本
function getRepeatText(repeatType, repeatDays) {
  if (repeatType === 'none') return '不重复'
  if (repeatType === 'daily') return '每天'
  if (repeatType === 'workday') return '法定工作日'
  if (repeatType === 'holiday') return '法定节假日'
  if (repeatType === 'custom') {
    const dayMap = {
      '0': '周日',
      '1': '周一',
      '2': '周二',
      '3': '周三',
      '4': '周四',
      '5': '周五',
      '6': '周六'
    }
    return `自定义: ${repeatDays?.map(day => dayMap[day]).join(', ')}`
  }
  return '不重复'
}

// 页面加载时执行
onMounted(() => {
  // 模拟加载任务数据
  setTimeout(() => {
    tasks.value = [
      // 这里可以添加示例任务数据
    ]
  }, 500)

  // 处理URL参数
  handleUrlParams()
})

// 处理URL参数
function handleUrlParams() {
  const params = new URLSearchParams(window.location.search)
  if (params.has('recipient') && params.has('sendTime') && params.has('messageContent')) {
    formData.recipient = params.get('recipient')
    formData.sendTime = params.get('sendTime')
    formData.repeatType = params.get('repeatType') || 'none'
    formData.messageContent = params.get('messageContent')
    charCount.value = formData.messageContent.length

    if (params.has('repeatDays')) {
      formData.repeatDays = params.get('repeatDays').split(',')
    }
  }
}
</script>

<style scoped>
:root {
    --primary-color: #4f46e5; /* 主色调 - 现代蓝紫色 */
    --primary-light: #818cf8; /* 亮主色调 */
    --primary-dark: #3730a3; /* 暗主色调 */
    --primary-glow: rgba(79, 70, 229, 0.15); /* 主色调发光效果 */
    --gradient-primary: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); /* 主色调渐变 */
    --text-color: #1e293b; /* 文本颜色 */
    --text-muted: #64748b; /* 次要文本颜色 */
    --background-color: #f8fafc; /* 背景色 */
    --card-bg-color: #ffffff; /* 卡片背景色 */
    --border-color: #e2e8f0; /* 边框颜色 */
    --shadow: 0 4px 12px rgba(0, 0, 0, 0.05); /* 阴影 */
    --shadow-hover: 0 10px 25px rgba(0, 0, 0, 0.08); /* 悬停阴影 */
    --spacing-xs: 8px; /* 超小间距 */
    --spacing-sm: 12px; /* 小间距 */
    --spacing-md: 16px; /* 中等间距 */
    --spacing-lg: 24px; /* 大间距 */
    --spacing-xl: 32px; /* 超大间距 */
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* 过渡效果 */
    --border-radius: 12px; /* 边框圆角 */
    --border-radius-sm: 8px; /* 小边框圆角 */
    --error-color: #ef4444; /* 错误颜色 */
    --success-color: #10b981; /* 成功颜色 */
    --warning-color: #f59e0b; /* 警告颜色 */
    --info-color: #3b82f6; /* 信息颜色 */
}

/* 暗色模式 */
body.dark-mode {
    --primary-color: #818cf8; /* 暗色主色调 */
    --primary-light: #a5b4fc; /* 暗色亮主色调 */
    --primary-dark: #4f46e5; /* 暗色暗主色调 */
    --primary-glow: rgba(129, 140, 248, 0.15); /* 暗色主色调发光效果 */
    --gradient-primary: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%); /* 暗色主色调渐变 */
    --text-color: #f1f5f9; /* 暗色文本颜色 */
    --text-muted: #94a3b8; /* 暗色次要文本颜色 */
    --background-color: #0f172a; /* 暗色背景色 */
    --card-bg-color: #1e293b; /* 暗色卡片背景色 */
    --border-color: #334155; /* 暗色边框 */
    --shadow: 0 4px 12px rgba(0, 0, 0, 0.15); /* 暗色模式阴影 */
}

/* 动画效果 */
.animate-fade-in { animation: fadeIn 0.5s ease forwards; }
.animate-fade-out { animation: fadeOut 0.3s ease forwards; }
.animate-slide-up { animation: slideUp 0.4s ease forwards; }
.animate-pulse { animation: pulse 2s infinite; }
.animate-scale { transition: transform 0.3s ease; }
.animate-scale:hover { transform: scale(1.02); }

@keyframes fadeIn {
    from { opacity: 0; }    to { opacity: 1; }
}

@keyframes fadeOut {
    from { opacity: 1; transform: scale(1); }    to { opacity: 0; transform: scale(0.95); }
}

@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }    to { transform: translateY(0); opacity: 1; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }    50% { opacity: 0.7; }
}

/* 基础样式重置 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
    padding: 0;
    transition: background-color var(--transition), color var(--transition);
}

/* 主容器样式 */
.auto-info-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* 页面标题区域 */
.page-header {
    margin-bottom: var(--spacing-xl);
    padding: var(--spacing-lg) 0;
    border-bottom: 1px solid var(--border-color);
}

/* 任务创建卡片 */
.task-creation-card {
    background-color: var(--card-bg-color);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
    border: 1px solid var(--border-color);
}

.card-header {
    margin-bottom: var(--spacing-lg);
}

.card-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--spacing-xs);
    display: flex;
    align-items: center;
}

.card-subtitle {
    color: var(--text-muted);
    font-size: 0.875rem;
}

/* 表单样式 */
.el-form {
    width: 100%;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--spacing-lg);
    margin-bottom: 0;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: var(--spacing-md);
    margin-top: var(--spacing-lg);
}

.actions-separator {
    flex-grow: 1;
}

.field-hint {
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-top: var(--spacing-xs);
}

/* 任务列表区域 */
.task-list-container {
    background-color: var(--card-bg-color);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
    padding: var(--spacing-lg);
    border: 1px solid var(--border-color);
}

.task-list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-sm);
    border-bottom: 1px solid var(--border-color);
}

.task-list-actions {
    display: flex;
    gap: var(--spacing-sm);
}

.task-list {
    list-style: none;
}

.task-item {
    background-color: var(--card-bg-color);
    border-radius: var(--border-radius);
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    box-shadow: var(--shadow);
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: var(--transition);
    border: 1px solid var(--border-color);
}

.task-item:hover {
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
    border-color: var(--primary-light);
}

.task-content {
    flex: 1;
}

.task-recipient {
    font-weight: 600;
    margin-bottom: var(--spacing-xs);
}

.task-message {
    color: var(--text-color);
    margin-bottom: var(--spacing-xs);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.task-meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-sm);
    font-size: 0.875rem;
    color: var(--text-muted);
}

.task-status {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
}

.task-status.pending {
    background-color: rgba(59, 130, 246, 0.1);
    color: var(--info-color);
}

.task-status.completed {
    background-color: rgba(16, 185, 129, 0.1);
    color: var(--success-color);
}

/* 空状态样式 */
.empty-task-state {
    text-align: center;
    padding: var(--spacing-xl) 0;
}

.empty-state-image {
    margin-bottom: var(--spacing-lg);
}

.empty-state-icon {
    width: 120px;
    height: 120px;
    opacity: 0.5;
}

.empty-state-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: var(--spacing-xs);
}

.empty-state-description {
    color: var(--text-muted);
    max-width: 300px;
    margin: 0 auto;
}

/* 通知容器样式 */
.notification-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    width: 300px;
}

/* 确保Element Plus组件样式与原项目一致 */
.el-input__inner,
.el-textarea__inner,
.el-button {
  border-radius: var(--border-radius-sm);
}

.el-button {
  padding: var(--spacing-sm) var(--spacing-md);
}
</style>