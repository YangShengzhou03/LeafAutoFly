<template>
  <div class="auto-info-container">
    <section class="task-creation-section">
      <el-card class="task-creation-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>创建新任务</span>
          </div>
        </template>
        
        <el-form ref="taskForm" :model="formData" :rules="rules" label-width="100px">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="12" :lg="12">
              <el-form-item label="接收者" prop="recipient">
                <el-input
                  v-model="formData.recipient"
                  placeholder="输入接收者信息"
                  clearable
                >
                  <template #prefix>
                    <el-icon><User /></el-icon>
                  </template>
                </el-input>
                <div class="el-form-item__tip">多个接收者用逗号分隔</div>
              </el-form-item>
            </el-col>

            <el-col :xs="24" :sm="12" :md="12" :lg="12">
              <el-form-item label="发送时间" prop="sendTime">
                <el-date-picker
                  v-model="formData.sendTime"
                  type="datetime"
                  placeholder="选择发送时间"
                  value-format="YYYY-MM-DDTHH:mm"
                  :default-value="defaultDateTime"
                  style="width: 100%"
                />
                <div class="el-form-item__tip">选择发送时间，到点就会发送</div>
              </el-form-item>
            </el-col>

            <el-col :xs="24" :sm="12" :md="12" :lg="12">
              <el-form-item label="重复选项">
                <el-select
                  v-model="formData.repeatType"
                  placeholder="选择重复类型"
                  style="width: 100%"
                >
                  <el-option
                    v-for="option in repeatOptions"
                    :key="option.value"
                    :label="option.label"
                    :value="option.value"
                  />
                </el-select>
                <div v-if="formData.repeatType === 'custom'" class="custom-days">
                  <p class="el-form-item__tip">选择重复日期：</p>
                  <el-checkbox-group v-model="formData.repeatDays">
                    <el-checkbox
                      v-for="day in daysOfWeek"
                      :key="day.value"
                      :label="day.value"
                    >
                      {{ day.label }}
                    </el-checkbox>
                  </el-checkbox-group>
                </div>
                <div class="el-form-item__tip">像定闹钟一样，选择重复日期</div>
              </el-form-item>
            </el-col>

            <el-col :span="24">
              <el-form-item label="信息内容" prop="messageContent" required>
                <el-input
                  v-model="formData.messageContent"
                  type="textarea"
                  placeholder="输入信息内容"
                  :rows="4"
                  show-word-limit
                  maxlength="500"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item>
            <el-button type="default" @click="resetForm">重置</el-button>
            <el-button type="primary" @click="submitForm">
              创建任务
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </section>

    <section class="task-list-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <div class="header-title">
              <span>任务列表</span>
              <span class="task-count">({{ tasks.length }})</span>
            </div>
            <div class="task-actions">
              <el-button-group>
                <el-button @click="refreshTasks">
                  <el-icon><Refresh /></el-icon>刷新
                </el-button>
                <el-button :disabled="tasks.length === 0">
                  导入
                </el-button>
                <el-button :disabled="tasks.length === 0">
                  导出
                </el-button>
                <el-button type="primary" :disabled="tasks.length === 0">
                  开始执行
                </el-button>
              </el-button-group>
            </div>
          </div>
        </template>

        <el-table
          v-if="tasks.length > 0"
          :data="sortedTasks"
          style="width: 100%"
          border
          stripe
          fit
          :row-class-name="tableRowClassName"
        >
          <el-table-column prop="recipient" label="接收者" min-width="20px" />
          <el-table-column prop="messageContent" label="内容" min-width="20px">
            <template #default="{ row }">
              <el-tooltip :content="row.messageContent" placement="top">
                <div class="message-content">{{ row.messageContent }}</div>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="sendTime" label="发送时间" min-width="15px">
            <template #default="{ row }">
              {{ formatDateTime(row.sendTime) }}
            </template>
          </el-table-column>
          <el-table-column label="重复类型" min-width="20px">
            <template #default="{ row }">
              {{ getRepeatText(row.repeatType, row.repeatDays) }}
            </template>
          </el-table-column>
          <el-table-column label="状态" min-width="10px" fixed="right">
            <template #default="{ row }">
              <el-tag
                :type="row.status === 'pending' ? 'info' : 'success'"
                size="small"
              >
                {{ row.status === 'pending' ? '待执行' : '已完成' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="16px" fixed="right">
            <template #default="{ row }">
              <div class="operation-buttons">
                <el-button
                  type="primary"
                  size="small"
                  @click="editTask(row.id)"
                  :icon="Edit"
                >编辑</el-button>
                <el-button
                  type="danger"
                  size="small"
                  @click="deleteTask(row.id)"
                  :icon="Delete"
                >删除</el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <el-empty v-else description="快创建您的第一个自动信息任务">
        </el-empty>
      </el-card>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { 
  ElMessage, ElMessageBox, ElCard, ElForm, ElFormItem, ElInput, 
  ElDatePicker, ElSelect, ElOption, ElCheckboxGroup, ElCheckbox, 
  ElButton, ElButtonGroup, ElTable, ElTableColumn, ElTag, 
  ElTooltip, ElEmpty, ElIcon 
} from 'element-plus'
import { User, Delete, Refresh, Edit } from '@element-plus/icons-vue'

const formData = reactive({
  recipient: '',
  sendTime: '',
  repeatType: 'none',
  repeatDays: [],
  messageContent: ''
})

const rules = {
  recipient: [
    { required: true, message: '请输入接收者', trigger: 'blur' },
    { validator: (rule, value, callback) => {
      if (!value.trim()) {
        callback(new Error('请输入接收者'))
      } else {
        callback()
      }
    }, trigger: 'blur' }
  ],
  sendTime: [
    { required: true, message: '请选择发送时间', trigger: 'change' }
  ],
  messageContent: [
    { required: true, message: '请输入消息内容', trigger: 'blur' }
  ]
}


const tasks = ref([
  {
    id: 1,
    recipient: 'user1@example.com',
    sendTime: '2023-10-15T09:00',
    repeatType: 'daily',
    repeatDays: [],
    messageContent: '每日早上9点的例行提醒',
    status: 'pending'
  },
  {
    id: 2,
    recipient: 'user2@example.com,user3@example.com',
    sendTime: '2023-10-16T14:30',
    repeatType: 'workday',
    repeatDays: [],
    messageContent: '工作日下午2:30的团队会议提醒',
    status: 'pending'
  },
  {
    id: 3,
    recipient: 'user4@example.com',
    sendTime: '2023-10-14T18:00',
    repeatType: 'custom',
    repeatDays: ['1', '2', '3', '4', '5', '6', '0'],
    messageContent: '每周一、三、五下午6点的项目进度汇报',
    status: 'completed'
  }
])

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

const defaultDateTime = computed(() => {
  const now = new Date()
  now.setMinutes(now.getMinutes() + 30)
  return now
})

const sortedTasks = computed(() => {
  return [...tasks.value].sort((a, b) => new Date(a.sendTime) - new Date(b.sendTime))
})

const resetForm = () => {
  formData.recipient = ''
  formData.sendTime = ''
  formData.repeatType = 'none'
  formData.repeatDays = []
  formData.messageContent = ''
}

const submitForm = async () => {
  try {    
    if (formData.repeatType === 'custom' && formData.repeatDays.length === 0) {
      ElMessage.error('请至少选择一个重复日期')
      return
    }

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
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}


const tableRowClassName = ({ row }) => {
  return row.status === 'pending' ? 'task-pending' : 'task-completed';
}

const editTask = (taskId) => {
  // 找到要编辑的任务
  const task = tasks.value.find(t => t.id === taskId)
  if (task) {
    // 填充表单
    formData.recipient = task.recipient
    formData.sendTime = task.sendTime
    formData.repeatType = task.repeatType
    formData.repeatDays = task.repeatDays
    formData.messageContent = task.messageContent
    
    // 删除原任务
    tasks.value = tasks.value.filter(t => t.id !== taskId)
    
    ElMessage({ message: '请修改任务信息', type: 'info' })
  }
}

const deleteTask = (taskId) => {
  ElMessageBox.confirm('确定要删除这个任务吗？', '提示', {
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


const refreshTasks = () => {
  // 这里可以添加实际的刷新逻辑，例如从服务器获取最新任务
  ElMessage({ message: '任务列表已刷新', type: 'success', duration: 1000 });
}

const getRepeatText = (repeatType, repeatDays) => {
  const dayMap = {
    '0': '周日', '1': '周一', '2': '周二', '3': '周三',
    '4': '周四', '5': '周五', '6': '周六'
  }
  
  switch(repeatType) {
    case 'none': return '不重复'
    case 'daily': return '每天'
    case 'workday': return '法定工作日'
    case 'holiday': return '法定节假日'
    case 'custom': return `自定义: ${repeatDays?.map(day => dayMap[day]).join(', ')}`
    default: return '不重复'
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
}

/* 表格行样式 */
.task-pending .el-table__cell {
  background-color: rgba(59, 130, 246, 0.1);
}

.task-completed .el-table__cell {
  background-color: rgba(16, 185, 129, 0.1);
}

/* 动画效果 */
.task-creation-card, .task-list-section .el-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  background-color: white;
}

.task-creation-card:hover, .task-list-section .el-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px 0 rgba(0, 0, 0, 0.08), 0 2px 4px 0 rgba(0, 0, 0, 0.04);
  border-color: var(--primary-color);
}

/* 按钮悬停效果增强 */
.el-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(30, 64, 175, 0.2);
}

.el-button {
  transition: all 0.2s ease;
}

.el-button--primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.el-button--primary:hover {
  background-color: #1e3a8a;
  border-color: #1e3a8a;
}

.auto-info-container {
  padding: 0;
  max-width: 100vw;
  margin: 0 auto;
  background-color: var(--light-color);
  min-height: 100vh;
}

.task-creation-section {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
}

.card-header .span {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
  color: var(--text-primary);
}

.task-count {
  font-size: 12px;
  color: var(--text-secondary);
  background-color: var(--light-color);
  padding: 2px 8px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.task-actions {
  display: flex;
  gap: 10px;
  padding: 5px 0;
}

.message-content {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.operation-buttons {
  display: flex;
  gap: 6px;
  justify-content: center;
}

.operation-buttons .el-button {
  padding: 4px 8px;
  font-size: 12px;
}

.custom-days {
  margin-top: 10px;
  padding: 12px;
  background-color: white;
  border-radius: 6px;
  border: 1px solid var(--border-color);
}

.el-form-item__tip {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

/* 表格样式增强 */
.el-table {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
}

.el-table th {
  background-color: rgba(30, 64, 175, 0.05);
  font-weight: 600;
  color: var(--text-primary);
  padding: 12px 0;
}

.el-table td {
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.el-table tr:last-child td {
  border-bottom: none;
}

.el-table--enable-row-hover .el-table__body tr:hover > td {
  background-color: rgba(59, 130, 246, 0.08);
}

/* 固定列样式优化 */
.el-table__fixed-right {
  box-shadow: -2px 0 6px rgba(0, 0, 0, 0.05);
}

/* 标签样式 */
.el-tag--info {
  background-color: rgba(59, 130, 246, 0.1);
  color: var(--secondary-color);
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.el-tag--success {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .task-actions {
    width: 100%;
  }
  
  .el-button-group {
    display: flex;
    width: 100%;
  }
  
  .el-button-group .el-button {
    flex: 1;
  }
}
</style>
