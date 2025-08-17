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
/* 这里可以添加组件特定样式 */
/* 大部分样式已经在auto_info.css中定义，这里只需要添加必要的覆盖样式 */

/* 确保Element Plus组件样式与原项目一致 */
.el-input__inner,
.el-textarea__inner,
.el-button {
  border-radius: var(--border-radius-sm);
}

.el-button {
  padding: var(--spacing-sm) var(--spacing-md);
}

/* 调整表单布局 */
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

/* 任务项样式 */
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

/* 其他样式保持与原项目一致 */
</style>