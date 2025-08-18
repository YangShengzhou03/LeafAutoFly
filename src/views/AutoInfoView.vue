<template>
  <div class="auto-info-container">
    <div class="notification-container" ref="notificationContainer"></div>

    <section class="task-creation-section">
      <div class="section-header">
        <h2>创建新任务</h2>
        <p>设置自动发送的信息内容、接收者和发送时间</p>
      </div>
      <div class="task-creation-card animate-fade-in">
        <el-form ref="taskForm" :model="formData" :rules="rules" label-width="100px">
          <div class="form-grid">
            <el-form-item label="接收者" prop="recipient" required>
              <el-input
                v-model="formData.recipient"
                placeholder="输入接收者信息"
                clearable
                class="form-input"
              >
                <template #suffix>
                  <el-icon class="contact-icon"><User /></el-icon>
                </template>
              </el-input>
              <div class="field-hint">多个接收者用逗号分隔</div>
            </el-form-item>

            <el-form-item label="发送时间" prop="sendTime" required>
              <el-date-picker
                v-model="formData.sendTime"
                type="datetime"
                placeholder="选择发送时间"
                value-format="YYYY-MM-DDTHH:mm"
                :default-value="defaultDateTime"
                class="form-input"
              ></el-date-picker>
            </el-form-item>

            <el-form-item label="重复选项">
              <el-select
                v-model="formData.repeatType"
                placeholder="选择重复类型"
                class="form-input"
              >
                <el-option
                  v-for="option in repeatOptions"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                ></el-option>
              </el-select>
              <div v-if="formData.repeatType === 'custom'" class="custom-days mt-2">
                <p class="form-text mb-1">选择重复日期：</p>
                <div class="day-selector">
                  <el-checkbox-group v-model="formData.repeatDays" class="flex-wrap gap-2">
                    <el-checkbox
                      v-for="day in daysOfWeek"
                      :key="day.value"
                      :label="day.value"
                      class="mr-2"
                    >
                      {{ day.label }}
                    </el-checkbox>
                  </el-checkbox-group>
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
                class="form-input"
              ></el-input>
              <div class="char-count">{{ charCount }}/500</div>
            </el-form-item>
          </div>

          <div class="form-actions">
            <el-button type="default" @click="resetForm" class="reset-btn">重置</el-button>
            <el-button type="primary" @click="submitForm" class="submit-btn">
              <el-icon class="mr-1"><Send /></el-icon> 创建任务
            </el-button>
          </div>
        </el-form>
      </div>
    </section>

    <section class="task-list-section">
      <div class="section-header">
        <h2>任务列表</h2>
        <p>当前共有 {{ tasks.length }} 个任务</p>
      </div>
      <div class="task-list-actions mb-4">
        <el-button type="primary" plain :disabled="tasks.length === 0" class="mr-2">
          <el-icon class="mr-1"><Import /></el-icon> 导入
        </el-button>
        <el-button type="primary" plain :disabled="tasks.length === 0" class="mr-2">
          <el-icon class="mr-1"><Export /></el-icon> 导出
        </el-button>
        <el-button type="primary" :disabled="tasks.length === 0">
          <el-icon class="mr-1"><Play /></el-icon> 开始执行
        </el-button>
      </div>

      <el-table
        v-if="tasks.length > 0"
        :data="sortedTasks"
        style="width: 100%"
        class="task-table"
        :row-class-name="taskRowClassName"
      >
        <el-table-column prop="recipient" label="接收者" width="180"></el-table-column>
        <el-table-column prop="messageContent" label="内容" width="300">
          <template #default="{ row }">
            <div class="message-content" :title="row.messageContent">{{ row.messageContent }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="sendTime" label="发送时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.sendTime) }}
          </template>
        </el-table-column>
        <el-table-column label="重复类型" width="150">
          <template #default="{ row }">
            {{ getRepeatText(row.repeatType, row.repeatDays) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag
              :type="row.status === 'pending' ? 'info' : 'success'"
              size="small"
            >
              {{ row.status === 'pending' ? '待执行' : '已完成' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button
              type="danger"
              size="small"
              @click="deleteTask(row.id)"
            >
              <el-icon><Delete /></el-icon>
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="empty-task-state" v-else>
        <div class="empty-state-image animate-fade-in">
          <img src="../assets/images/empty-tasks.svg" alt="暂无任务" class="empty-state-icon">
        </div>
        <h3 class="empty-state-title">暂无任务</h3>
        <p class="empty-state-description">点击上方的"创建新任务"按钮，开始创建您的第一个自动信息任务</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElTag, ElForm, ElFormItem, ElInput, ElDatePicker, ElSelect, ElOption, ElCheckboxGroup, ElCheckbox, ElButton, ElTable, ElTableColumn, ElIcon } from 'element-plus'
import { User, Send, Play, Import, Export, Delete } from '@element-plus/icons-vue'

const formData = reactive({
  recipient: '',
  sendTime: '',
  repeatType: 'none',
  repeatDays: [],
  messageContent: ''
})

const validateRecipient = (rule, value, callback) => {
  if (!value.trim()) {
    callback(new Error('请输入接收者'))
    return
  }
  callback()
}

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

const tasks = ref([])

const repeatOptions = [
  { label: '不重复', value: 'none' },
  { label: '每天', value: 'daily' },
  { label: '法定工作日', value: 'workday' },
  { label: '法定节假日', value: 'holiday' },
  { label: '自定义', value: 'custom' }
]

const daysOfWeek = [
  { label: '周一', value: '1' },
  { label: '周二', value: '2' },
  { label: '周三', value: '3' },
  { label: '周四', value: '4' },
  { label: '周五', value: '5' },
  { label: '周六', value: '6' },
  { label: '周日', value: '0' }
]

const charCount = ref(0)

const defaultDateTime = computed(() => {
  const now = new Date()
  now.setMinutes(now.getMinutes() + 30)
  return now
})

const sortedTasks = computed(() => {
  return [...tasks.value].sort((a, b) => new Date(a.sendTime) - new Date(b.sendTime))
})

const updateCharCount = () => {
  charCount.value = formData.messageContent.length
  if (charCount.value > 500) {
    formData.messageContent = formData.messageContent.substring(0, 500)
    charCount.value = 500
  }
}

const resetForm = () => {
  formData.recipient = ''
  formData.sendTime = ''
  formData.repeatType = 'none'
  formData.repeatDays = []
  formData.messageContent = ''
  charCount.value = 0
  const taskForm = document.querySelector('[ref="taskForm"]')
  if (taskForm && taskForm.resetFields) {
    taskForm.resetFields()
  }
}

const submitForm = () => {
  const taskForm = document.querySelector('[ref="taskForm"]')
  if (taskForm && taskForm.validate) {
    taskForm.validate((valid) => {
      if (valid) {
        if (formData.repeatType === 'custom' && formData.repeatDays.length === 0) {
          ElMessage.error('请至少选择一个重复日期')
          return
        }

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
    })
  } else {
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

const deleteTask = (taskId) => {
  ElMessage.confirm('确定要删除这个任务吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    tasks.value = tasks.value.filter(task => task.id !== taskId)
    ElMessage.success('任务删除成功')
  }).catch(() => {})
}

const formatDateTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return dateString
  return `${date.getFullYear()}-${padZero(date.getMonth() + 1)}-${padZero(date.getDate())} ${padZero(date.getHours())}:${padZero(date.getMinutes())}`
}

const padZero = (num) => {
  return num < 10 ? '0' + num : num
}

const getRepeatText = (repeatType, repeatDays) => {
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

const taskRowClassName = ({ rowIndex }) => {
  return rowIndex % 2 === 0 ? 'even-row' : 'odd-row'
}

onMounted(() => {
  setTimeout(() => {
    tasks.value = [
      {
        id: Date.now() - 3600000,
        recipient: '张三, 李四',
        sendTime: new Date(Date.now() + 3600000).toISOString().slice(0, 16),
        repeatType: 'daily',
        repeatDays: [],
        messageContent: '这是一条每日提醒消息，请注意查收。',
        status: 'pending'
      },
      {
        id: Date.now() - 7200000,
        recipient: '王五',
        sendTime: new Date(Date.now() + 7200000).toISOString().slice(0, 16),
        repeatType: 'custom',
        repeatDays: ['1', '3', '5'],
        messageContent: '每周一、三、五的工作汇报提醒，请按时提交。',
        status: 'pending'
      }
    ]
  }, 500)

  handleUrlParams()
})

const handleUrlParams = () => {
  try {
    const params = new URLSearchParams(window.location.search)
    if (params.has('recipient') && params.has('sendTime') && params.has('messageContent')) {
      formData.recipient = decodeURIComponent(params.get('recipient') || '')
      formData.sendTime = params.get('sendTime') || ''
      formData.repeatType = params.get('repeatType') || 'none'
      formData.messageContent = decodeURIComponent(params.get('messageContent') || '')
      charCount.value = formData.messageContent.length

      if (params.has('repeatDays')) {
        formData.repeatDays = params.get('repeatDays').split(',')
      }
    }
  } catch (error) {
    console.error('处理URL参数时出错:', error)
  }
}
</script>

<style scoped>
:root {
  --primary-color: #1e40af;
  --secondary-color: #3b82f6;
  --accent-color: #2563eb;
  --light-color: #f8fafc;
  --dark-color: #1e293b;
  --text-primary: #0f172a;
  --text-secondary: #64748b;
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --border-color: #e2e8f0;
  --card-bg: #ffffff;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --transition: all 0.3s ease;
}

.animate-fade-in { animation: fadeIn 0.5s ease forwards; }
.animate-slide-up { animation: slideUp 0.5s ease forwards; }

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

* {
  margin: 0; padding: 0; box-sizing: border-box;
}

.auto-info-container {
  max-width: 1200px; margin: 0 auto; padding: 20px;
  font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background-color: var(--light-color);
  min-height: 100vh;
}

.section-header {
  text-align: center; margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.8rem; font-weight: 700; color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.section-header p {
  font-size: 1rem; color: var(--text-secondary);
  max-width: 700px; margin: 0 auto;
}

.task-creation-section {
  margin-bottom: 3rem;
}

.task-creation-card {
  background-color: var(--card-bg);
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 2rem;
  transition: var(--transition);
  border: 1px solid var(--border-color);
}

.task-creation-card:hover {
  box-shadow: var(--shadow-hover);
}

.form-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem; margin-bottom: 1.5rem;
}

.full-width {
  grid-column: 1 / -1;
}

.form-actions {
  display: flex; justify-content: flex-end; gap: 1rem;
  margin-top: 1.5rem;
}

.char-count {
  text-align: right; font-size: 0.875rem; color: var(--text-secondary);
  margin-top: 0.5rem;
}

.task-list-section {
  margin-bottom: 2rem;
}

.task-list-actions {
  display: flex;
}

.task-table {
  background-color: var(--card-bg);
  border-radius: 8px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.message-content {
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.empty-task-state {
  text-align: center; padding: 3rem 0;
}

.empty-state-image {
  margin-bottom: 1.5rem;
}

.empty-state-icon {
  max-width: 150px; opacity: 0.7;
}

.empty-state-title {
  font-size: 1.25rem; font-weight: 600; color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.empty-state-description {
  color: var(--text-secondary); max-width: 400px; margin: 0 auto;
}

.even-row {
  background-color: rgba(248, 250, 252, 0.5);
}

.odd-row {
  background-color: var(--card-bg);
}

.field-hint {
  font-size: 0.875rem; color: var(--text-secondary);
  margin-top: 0.25rem;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .task-list-actions {
    flex-direction: column;
    gap: 1rem;
  }

  .task-list-actions .el-button {
    width: 100%;
  }
}
</style>
