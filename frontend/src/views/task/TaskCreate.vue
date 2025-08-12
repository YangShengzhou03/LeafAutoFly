<template>
  <div class="task-create-container">
    <el-card class="task-form-card">
      <template #header>
        <div class="card-header">
          <span>创建新任务</span>
        </div>
      </template>

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

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="handleCancel" style="margin-left: 10px;">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Save, Cancel }
  from '@element-plus/icons-vue'

// 响应式数据
const taskForm = ref({
  title: '',
  description: '',
  status: 'pending',
  priority: 'medium',
  dueTime: '',
  assignee: ''
})

const taskFormRef = ref(null)
const router = useRouter()
const taskRules = {
  title: [
    {
      required: true,
      message: '请输入任务标题',
      trigger: 'blur'
    }
  ],
  description: [
    {
      required: true,
      message: '请输入任务描述',
      trigger: 'blur'
    }
  ],
  dueTime: [
    {
      required: true,
      message: '请选择截止时间',
      trigger: 'blur'
    }
  ],
  assignee: [
    {
      required: true,
      message: '请输入负责人',
      trigger: 'blur'
    }
  ]
}

// 处理提交
const handleSubmit = () => {
  taskFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟提交表单
      setTimeout(() => {
        ElMessage.success('任务创建成功')
        router.push('/task/list')
      }, 800)
    }
  })
}

// 处理取消
const handleCancel = () => {
  router.go(-1)
}
</script>

<style scoped>
.task-create-container {
  padding: 20px;
}

.task-form-card {
  max-width: 600px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>