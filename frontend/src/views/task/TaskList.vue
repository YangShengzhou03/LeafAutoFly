<template>
  <div class="task-list-container">
    <el-card class="filter-card">
      <div class="filter-container">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索任务..."
          prefix-icon="Search"
          style="width: 20%"
        ></el-input>
        <el-select
          v-model="statusFilter"
          placeholder="任务状态"
          style="width: 15%; margin-left: 10px"
        >
          <el-option label="全部" value="all"></el-option>
          <el-option label="待处理" value="pending"></el-option>
          <el-option label="进行中" value="in_progress"></el-option>
          <el-option label="已完成" value="completed"></el-option>
          <el-option label="已取消" value="cancelled"></el-option>
        </el-select>
        <el-select
          v-model="priorityFilter"
          placeholder="优先级"
          style="width: 15%; margin-left: 10px"
        >
          <el-option label="全部" value="all"></el-option>
          <el-option label="高" value="high"></el-option>
          <el-option label="中" value="medium"></el-option>
          <el-option label="低" value="low"></el-option>
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          style="width: 30%; margin-left: 10px"
        ></el-date-picker>
        <el-button
          type="primary"
          @click="handleSearch"
          style="margin-left: 10px"
        >
          搜索
        </el-button>
        <el-button
          type="primary"
          plain
          @click="handleReset"
          style="margin-left: 10px"
        >
          重置
        </el-button>
      </div>
    </el-card>

    <el-card class="action-card">
      <div class="action-container">
        <el-button
          type="primary"
          @click="handleCreateTask"
          icon="Plus"
        >
          新建任务
        </el-button>
        <el-button
          type="primary"
          plain
          @click="handleBatchDelete"
          :disabled="selectedTaskIds.length === 0"
          icon="Delete"
          style="margin-left: 10px"
        >
          批量删除
        </el-button>
        <el-button
          type="primary"
          plain
          @click="handleExport"
          icon="Download"
          style="margin-left: 10px"
        >
          导出数据
        </el-button>
      </div>
    </el-card>

    <el-card class="task-table-card">
      <el-table
        v-loading="loading"
        :data="filteredTasks"
        style="width: 100%"
        border
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="id" label="任务ID" width="80"></el-table-column>
        <el-table-column prop="title" label="任务标题" min-width="180"></el-table-column>
        <el-table-column prop="description" label="任务描述" min-width="200"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag
              :type="{
                pending: 'warning',
                in_progress: 'primary',
                completed: 'success',
                cancelled: 'danger'
              }[scope.row.status]"
            >
              {{ {
                pending: '待处理',
                in_progress: '进行中',
                completed: '已完成',
                cancelled: '已取消'
              }[scope.row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="scope">
            <el-tag
              :type="{
                high: 'danger',
                medium: 'warning',
                low: 'success'
              }[scope.row.priority]"
              size="small"
            >
              {{ {
                high: '高',
                medium: '中',
                low: '低'
              }[scope.row.priority] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180"></el-table-column>
        <el-table-column prop="dueTime" label="截止时间" width="180"></el-table-column>
        <el-table-column prop="assignee" label="负责人" width="120"></el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="handleViewTask(scope.row)"
            >
              查看
            </el-button>
            <el-button
              type="primary"
              size="small"
              @click="handleEditTask(scope.row)"
              style="margin-left: 10px"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleDeleteTask(scope.row.id)"
              style="margin-left: 10px"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalTasks"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </el-card>

    <!-- 新建/编辑任务对话框 -->
    <el-dialog
      v-model="taskDialogVisible"
      :title="isEditTask ? '编辑任务' : '新建任务'"
      width="600px"
    >
      <el-form
        ref="taskFormRef"
        :model="taskForm"
        :rules="taskRules"
        label-width="100px"
      >
        <el-form-item prop="title">
          <el-input
            v-model="taskForm.title"
            placeholder="请输入任务标题"
          ></el-input>
        </el-form-item>
        <el-form-item prop="description">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            placeholder="请输入任务描述"
            rows="4"
          ></el-input>
        </el-form-item>
        <el-form-item prop="status">
          <el-select v-model="taskForm.status" placeholder="请选择任务状态">
            <el-option label="待处理" value="pending"></el-option>
            <el-option label="进行中" value="in_progress"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="priority">
          <el-select v-model="taskForm.priority" placeholder="请选择优先级">
            <el-option label="高" value="high"></el-option>
            <el-option label="中" value="medium"></el-option>
            <el-option label="低" value="low"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="dueTime">
          <el-date-picker
            v-model="taskForm.dueTime"
            type="datetime"
            placeholder="请选择截止时间"
          ></el-date-picker>
        </el-form-item>
        <el-form-item prop="assignee">
          <el-input
            v-model="taskForm.assignee"
            placeholder="请输入负责人"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="taskDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleSaveTask"
          :loading="taskSaving"
        >
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 查看任务对话框 -->
    <el-dialog
      v-model="viewTaskDialogVisible"
      title="任务详情"
      width="600px"
    >
      <div v-if="currentTask">
        <div class="detail-item">
          <span class="detail-label">任务ID:</span>
          <span class="detail-value">{{ currentTask.id }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">任务标题:</span>
          <span class="detail-value">{{ currentTask.title }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">任务描述:</span>
          <span class="detail-value">{{ currentTask.description }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">状态:</span>
          <span class="detail-value">
            <el-tag
              :type="{
                pending: 'warning',
                in_progress: 'primary',
                completed: 'success',
                cancelled: 'danger'
              }[currentTask.status]"
            >
              {{ {
                pending: '待处理',
                in_progress: '进行中',
                completed: '已完成',
                cancelled: '已取消'
              }[currentTask.status] }}
            </el-tag>
          </span>
        </div>
        <div class="detail-item">
          <span class="detail-label">优先级:</span>
          <span class="detail-value">
            <el-tag
              :type="{
                high: 'danger',
                medium: 'warning',
                low: 'success'
              }[currentTask.priority]"
              size="small"
            >
              {{ {
                high: '高',
                medium: '中',
                low: '低'
              }[currentTask.priority] }}
            </el-tag>
          </span>
        </div>
        <div class="detail-item">
          <span class="detail-label">创建时间:</span>
          <span class="detail-value">{{ currentTask.createTime }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">截止时间:</span>
          <span class="detail-value">{{ currentTask.dueTime }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">负责人:</span>
          <span class="detail-value">{{ currentTask.assignee }}</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="viewTaskDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Plus, Delete, Download, Edit, Eye }
  from '@element-plus/icons-vue'

// 响应式数据
const searchKeyword = ref('')
const statusFilter = ref('all')
const priorityFilter = ref('all')
const dateRange = ref([])
const tasks = ref([])
const loading = ref(false)
const selectedTaskIds = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const totalTasks = ref(0)
const taskDialogVisible = ref(false)
const viewTaskDialogVisible = ref(false)
const isEditTask = ref(false)
const currentTaskId = ref(null)
const currentTask = ref(null)
const taskForm = ref({
  title: '',
  description: '',
  status: 'pending',
  priority: 'medium',
  dueTime: '',
  assignee: ''
})
const taskFormRef = ref(null)
const taskSaving = ref(false)
const taskRules = {
  title: [
    {
      required: true,
      message: '请输入任务标题',
      trigger: 'blur'
    }
  ],
  dueTime: [
    {
      required: true,
      message: '请选择截止时间',
      trigger: 'blur'
    }
  ]
}

// 计算属性 - 过滤后的任务列表
const filteredTasks = computed(() => {
  let result = [...tasks.value]

  // 搜索关键词过滤
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(
      (task) =>
        task.title.toLowerCase().includes(keyword) ||
        task.description.toLowerCase().includes(keyword) ||
        task.assignee.toLowerCase().includes(keyword)
    )
  }

  // 状态过滤
  if (statusFilter.value !== 'all') {
    result = result.filter((task) => task.status === statusFilter.value)
  }

  // 优先级过滤
  if (priorityFilter.value !== 'all') {
    result = result.filter((task) => task.priority === priorityFilter.value)
  }

  // 日期范围过滤
  if (dateRange.value.length === 2) {
    const startDate = new Date(dateRange.value[0])
    const endDate = new Date(dateRange.value[1])
    endDate.setHours(23, 59, 59, 999)

    result = result.filter((task) => {
      const createTime = new Date(task.createTime)
      return createTime >= startDate && createTime <= endDate
    })
  }

  // 分页处理
  totalTasks.value = result.length
  return result.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

// 生命周期钩子
onMounted(() => {
  fetchTasks()
})

// 模拟获取任务数据
const fetchTasks = () => {
  loading.value = true

  // 模拟API请求延迟
  setTimeout(() => {
    const mockTasks = [
      {
        id: 1,
        title: '系统优化',
        description: '对系统性能进行全面优化',
        status: 'in_progress',
        priority: 'high',
        createTime: '2023-11-10 10:00:00',
        dueTime: '2023-11-20 18:00:00',
        assignee: '张三'
      },
      {
        id: 2,
        title: '用户界面设计',
        description: '设计新的用户界面原型',
        status: 'pending',
        priority: 'medium',
        createTime: '2023-11-11 14:30:00',
        dueTime: '2023-11-15 17:00:00',
        assignee: '李四'
      },
      {
        id: 3,
        title: '数据库备份',
        description: '每周数据库备份',
        status: 'completed',
        priority: 'low',
        createTime: '2023-11-09 09:00:00',
        dueTime: '2023-11-09 10:00:00',
        assignee: '王五'
      },
      {
        id: 4,
        title: 'Bug修复',
        description: '修复登录页面的兼容性问题',
        status: 'in_progress',
        priority: 'high',
        createTime: '2023-11-12 09:30:00',
        dueTime: '2023-11-13 18:00:00',
        assignee: '赵六'
      },
      {
        id: 5,
        title: '需求分析',
        description: '分析新功能需求',
        status: 'pending',
        priority: 'medium',
        createTime: '2023-11-13 10:00:00',
        dueTime: '2023-11-16 17:00:00',
        assignee: '钱七'
      }
    ]

    tasks.value = mockTasks
    loading.value = false
  }, 800)
}

// 搜索按钮点击事件
const handleSearch = () => {
  currentPage.value = 1
  // 触发重新计算filteredTasks
}

// 重置按钮点击事件
const handleReset = () => {
  searchKeyword.value = ''
  statusFilter.value = 'all'
  priorityFilter.value = 'all'
  dateRange.value = []
  currentPage.value = 1
}

// 选择任务事件
const handleSelectionChange = (selection) => {
  selectedTaskIds.value = selection.map((task) => task.id)
}

// 分页大小变化事件
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

// 当前页变化事件
const handleCurrentChange = (current) => {
  currentPage.value = current
}

// 新建任务按钮点击事件
const handleCreateTask = () => {
  isEditTask.value = false
  currentTaskId.value = null
  taskForm.value = {
    title: '',
    description: '',
    status: 'pending',
    priority: 'medium',
    dueTime: '',
    assignee: ''
  }
  taskDialogVisible.value = true
}

// 编辑任务按钮点击事件
const handleEditTask = (task) => {
  isEditTask.value = true
  currentTaskId.value = task.id
  taskForm.value = {
    title: task.title,
    description: task.description,
    status: task.status,
    priority: task.priority,
    dueTime: task.dueTime,
    assignee: task.assignee
  }
  taskDialogVisible.value = true
}

// 查看任务按钮点击事件
const handleViewTask = (task) => {
  currentTask.value = task
  viewTaskDialogVisible.value = true
}

// 删除任务按钮点击事件
const handleDeleteTask = (id) => {
  ElMessage.confirm('确定要删除该任务吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 模拟删除操作
    loading.value = true
    setTimeout(() => {
      tasks.value = tasks.value.filter((task) => task.id !== id)
      ElMessage.success('任务删除成功')
      loading.value = false
    }, 500)
  })
}

// 批量删除按钮点击事件
const handleBatchDelete = () => {
  ElMessage.confirm('确定要删除选中的任务吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 模拟批量删除操作
    loading.value = true
    setTimeout(() => {
      tasks.value = tasks.value.filter(
        (task) => !selectedTaskIds.value.includes(task.id)
      )
      selectedTaskIds.value = []
      ElMessage.success('任务批量删除成功')
      loading.value = false
    }, 500)
  })
}

// 导出数据按钮点击事件
const handleExport = () => {
  ElMessage.success('数据导出成功')
  // 实际应用中，这里应该调用导出API
}

// 保存任务按钮点击事件
const handleSaveTask = () => {
  taskFormRef.value.validate((valid) => {
    if (valid) {
      taskSaving.value = true

      // 模拟保存操作
      setTimeout(() => {
        if (isEditTask.value) {
          // 编辑任务
          const index = tasks.value.findIndex(
            (task) => task.id === currentTaskId.value
          )
          if (index !== -1) {
            tasks.value[index] = {
              ...tasks.value[index],
              ...taskForm.value
            }
          }
          ElMessage.success('任务编辑成功')
        } else {
          // 新建任务
          const newTask = {
            id: Date.now(), // 模拟唯一ID
            createTime: new Date().toLocaleString(),
            ...taskForm.value
          }
          tasks.value.unshift(newTask)
          ElMessage.success('任务创建成功')
        }

        taskDialogVisible.value = false
        taskSaving.value = false
      }, 800)
    }
  })
}
</script>

<style scoped>
.task-list-container {
  padding: 20px;
}

.filter-card,
.action-card,
.task-table-card {
  margin-bottom: 20px;
}

.filter-container {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.action-container {
  display: flex;
  align-items: center;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.detail-item {
  display: flex;
  margin-bottom: 15px;
}

.detail-label {
  width: 100px;
  font-weight: bold;
}

.detail-value {
  flex: 1;
}
</style>