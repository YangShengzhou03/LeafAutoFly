<template>
  <div class="ai-takeover-container">
    <div class="page-header">
      <h1>AI 接管设置</h1>
    </div>

    <div class="ai-settings-card animate-fade-in">
      <div class="card-header">
        <h2 class="card-title">
          <span class="ai-icon"></span>AI 自动回复配置
        </h2>
        <p class="card-subtitle">设置AI接管消息回复的相关参数和策略</p>
      </div>
      <div class="card-body">
        <el-form ref="aiForm" :model="formData" :rules="rules" label-width="150px">
          <el-form-item label="AI 接管状态" prop="aiStatus">
            <el-switch
              v-model="formData.aiStatus"
              active-color="var(--primary-color)"
              inactive-color="#ccc"
              active-text="启用"
              inactive-text="禁用"
            ></el-switch>
          </el-form-item>

          <el-form-item label="回复延迟 (秒)" prop="replyDelay">
            <el-input-number
              v-model="formData.replyDelay"
              :min="0"
              :max="30"
              :step="1"
              placeholder="输入回复延迟时间"
            ></el-input-number>
          </el-form-item>

          <el-form-item label="回复风格" prop="replyStyle">
            <el-select v-model="formData.replyStyle" placeholder="选择回复风格">
              <el-option label="正式" value="formal"></el-option>
              <el-option label="友好" value="friendly"></el-option>
              <el-option label="幽默" value="humorous"></el-option>
              <el-option label="专业" value="professional"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="最大回复长度" prop="maxReplyLength">
            <el-input-number
              v-model="formData.maxReplyLength"
              :min="10"
              :max="500"
              :step="10"
              placeholder="输入最大回复长度"
            ></el-input-number>
          </el-form-item>

          <el-form-item label="关键词过滤" prop="keywordFilter">
            <el-input
              v-model="formData.keywordFilter"
              placeholder="输入关键词，多个关键词用逗号分隔"
            ></el-input>
            <div class="field-hint">包含这些关键词的消息将被AI优先处理</div>
          </el-form-item>

          <el-form-item label="AI 回复模板" prop="replyTemplate">
            <el-input
              v-model="formData.replyTemplate"
              type="textarea"
              :rows="4"
              placeholder="输入AI回复模板"
            ></el-input>
            <div class="field-hint">使用 {content} 表示原始消息内容，{time} 表示当前时间</div>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitForm">保存设置</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <div class="ai-history-container">
      <div class="history-header">
        <h2>AI 回复历史</h2>
      </div>

      <el-table :data="replyHistory" style="width: 100%">
        <el-table-column prop="time" label="时间" width="180"></el-table-column>
        <el-table-column prop="originalMessage" label="原始消息" width="300"></el-table-column>
        <el-table-column prop="aiReply" label="AI 回复"></el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewDetails(scope.row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 表单数据
const formData = reactive({
  aiStatus: false,
  replyDelay: 5,
  replyStyle: 'friendly',
  maxReplyLength: 200,
  keywordFilter: '',
  replyTemplate: '感谢您的消息：{content}。此消息由AI自动回复，时间：{time}。'
})

// 表单验证规则
const rules = {
  replyDelay: [
    { required: true, message: '请输入回复延迟', trigger: 'blur' },
    { type: 'number', message: '回复延迟必须是数字', trigger: 'blur' },
    { min: 0, max: 30, message: '回复延迟必须在0-30秒之间', trigger: 'blur' }
  ],
  replyStyle: [
    { required: true, message: '请选择回复风格', trigger: 'change' }
  ],
  maxReplyLength: [
    { required: true, message: '请输入最大回复长度', trigger: 'blur' },
    { type: 'number', message: '最大回复长度必须是数字', trigger: 'blur' },
    { min: 10, max: 500, message: '最大回复长度必须在10-500之间', trigger: 'blur' }
  ],
  replyTemplate: [
    { required: true, message: '请输入AI回复模板', trigger: 'blur' }
  ]
}

// AI回复历史数据
const replyHistory = ref([
  {
    id: 1,
    time: '2023-11-15 10:30:25',
    originalMessage: '你好，请问什么时候发货？',
    aiReply: '感谢您的消息：你好，请问什么时候发货？。此消息由AI自动回复，时间：2023-11-15 10:30:25。'
  },
  {
    id: 2,
    time: '2023-11-15 09:15:42',
    originalMessage: '订单#12345什么时候能到？',
    aiReply: '感谢您的消息：订单#12345什么时候能到？。此消息由AI自动回复，时间：2023-11-15 09:15:42。'
  }
])

// 提交表单
function submitForm() {
  // 模拟API请求保存设置
  setTimeout(() => {
    ElMessage.success('AI设置保存成功')
  }, 500)
}

// 重置表单
function resetForm() {
  formData.aiStatus = false
  formData.replyDelay = 5
  formData.replyStyle = 'friendly'
  formData.maxReplyLength = 200
  formData.keywordFilter = ''
  formData.replyTemplate = '感谢您的消息：{content}。此消息由AI自动回复，时间：{time}。'
}

// 查看详情
function viewDetails(row) {
  ElMessage({
    message: `原始消息: ${row.originalMessage}\nAI回复: ${row.aiReply}`,
    type: 'info',
    duration: 5000
  })
}

// 页面加载时执行
onMounted(() => {
  // 模拟加载AI设置
  setTimeout(() => {
    // 这里可以添加从API加载设置的逻辑
  }, 500)
})
</script>

<style scoped>
.ai-takeover-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.ai-settings-card {
  background-color: var(--card-bg-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  border: 1px solid var(--border-color);
}

.ai-history-container {
  background-color: var(--card-bg-color);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: var(--spacing-lg);
  border: 1px solid var(--border-color);
}

.history-header {
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
}

/* 调整Element Plus表格样式 */
.el-table th,
.el-table td {
  padding: 12px;
}
</style>