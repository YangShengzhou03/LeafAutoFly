<template>
  <div class="app-container">
    
    <div class="main-content">
      
      <div class="top-row">
        
        <div class="config-card">
          <el-card class="config-card-inner" shadow="hover">
            <template #header>
              <div class="card-header">
                <div class="header-title">
                  <span>AI 自动回复配置</span>
                </div>
              </div>
            </template>

            <el-form ref="aiForm" :model="formData" :rules="rules" class="custom-input">
              <el-form-item label="AI接管状态" prop="aiStatus">
                <div class="status-toggle">
                  <el-switch v-model="formData.aiStatus" active-color="#3b82f6" inactive-color="#d1d5db" @change="toggleTakeover"></el-switch>
                  <div v-if="formData.aiStatus" class="takeover-time ml-3">
                    已接管: <span class="text-primary">{{ formattedTakeoverTime }}</span>
                  </div>
                </div>
              </el-form-item>

              <el-form-item label="回复延迟(秒)" prop="replyDelay">
                <el-input v-model.number="formData.replyDelay" placeholder="输入回复延迟时间"></el-input>
              </el-form-item>

              <el-form-item label="最小回复间隔(秒)" prop="minReplyInterval">
                <el-input v-model.number="formData.minReplyInterval" placeholder="输入最小回复间隔时间"></el-input>
              </el-form-item>

              <el-form-item label="接管联系人" prop="contactPerson">
                <el-input v-model="formData.contactPerson" placeholder="输入接管联系人姓名"></el-input>
              </el-form-item>

              <el-form-item label="AI人设" prop="aiPersona">
                <el-input v-model="formData.aiPersona" type="textarea" placeholder="描述AI的性格和回复风格" :rows="4"></el-input>
              </el-form-item>

              <div class="action-buttons">
                <el-button type="primary" :loading="isSubmitting" @click="submitForm" class="gradient-btn">保存设置</el-button>
                <el-button @click="resetForm">重置</el-button>
              </div>
            </el-form>
          </el-card>
        </div>

        
        <div class="insights-card">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <div class="header-title">
                  <span>AI 性能洞察</span>
                </div>
              </div>
            </template>

            <div class="card-body">
              <div class="stats-grid">
                <div class="stat-item">
                  <div class="stat-value counter" data-target="{{ stats.replyRate }}">{{ stats.replyRate }}%</div>
                  <div class="stat-label">回复率</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value counter" data-target="{{ stats.averageTime }}">{{ stats.averageTime }}s</div>
                  <div class="stat-label">平均响应时间</div>
                </div>
                <div class="stat-item">
                  <div class="stat-value counter" data-target="{{ stats.satisfactionRate }}">{{ stats.satisfactionRate }}%</div>
                  <div class="stat-label">满意度</div>
                </div>
              </div>
              <div class="chart-container">
                <div class="chart-card">
                  <div class="chart-header">
                    <h3>近7天AI回复数量趋势</h3>
                    <div class="chart-actions">
                      <el-select v-model="chartRange" placeholder="选择范围" size="small" class="chart-select">
                        <el-option label="7天" value="7d"></el-option>
                        <el-option label="30天" value="30d"></el-option>
                        <el-option label="90天" value="90d"></el-option>
                      </el-select>
                    </div>
                  </div>
                  <div class="chart-content">
                    <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="180" viewBox="0 0 400 180"><defs><linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#3b82f6" stop-opacity="0.4"/><stop offset="100%" stop-color="#3b82f6" stop-opacity="0"/></linearGradient></defs><path d="M0,150 Q50,120 100,130 T200,100 T300,120 T400,90" fill="url(#areaGradient)" stroke="#3b82f6" stroke-width="3" stroke-linecap="round"/><path d="M0,150 L400,150" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="4"/><circle cx="100" cy="130" r="4" fill="#ffffff" stroke="#3b82f6" stroke-width="2"/><circle cx="200" cy="100" r="4" fill="#ffffff" stroke="#3b82f6" stroke-width="2"/><circle cx="300" cy="120" r="4" fill="#ffffff" stroke="#3b82f6" stroke-width="2"/><circle cx="400" cy="90" r="4" fill="#ffffff" stroke="#3b82f6" stroke-width="2"/></svg>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 下方依次排列区域 -->
      
      <el-card class="rules-card" shadow="hover">
        <template #header>
              <div class="card-header">
                <div class="header-title">
                  <span>AI 自定义回复规则</span>
                </div>
              </div>
            </template>

        <div class="custom-rules-container">
          <div class="rule-actions">
            <el-button type="primary" @click="addRule" class="gradient-btn">添加规则</el-button>
          </div>

          <el-table v-model:data="formData.customRules" border class="rules-table" ref="rulesForm" row-key="id">
            <el-table-column prop="matchType" label="匹配类型" width="180">
              <template #default="{ row }">
                <el-select v-model="row.matchType" placeholder="选择匹配类型" size="small" class="custom-select">
                  <el-option label="包含关键词" value="contains"></el-option>
                  <el-option label="完全匹配" value="equals"></el-option>
                  <el-option label="正则表达式" value="regex"></el-option>
                </el-select>
              </template>
            </el-table-column>
            <el-table-column prop="keyword" label="关键词/规则" width="240">
              <template #default="{ row }"><!-- 移除未使用的$index变量 -->
                <el-input v-model="row.keyword" placeholder="输入关键词或规则" size="small" class="custom-input"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="reply" label="回复内容">
              <template #default="{ row }"><!-- 移除未使用的$index变量 -->
                <el-input v-model="row.reply" type="textarea" placeholder="输入回复内容" size="small" :rows="2" class="custom-input"></el-input>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100" fixed="right">
              <template #default="{ $index }">
                <div class="operation-buttons">
                  <el-button type="danger" size="small" @click="removeRule($index)" class="delete-btn">删除</el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>

      
      <el-card class="history-card" shadow="hover">
        <template #header>
              <div class="card-header">
                <div class="header-title">
                  <span>AI 回复历史</span>
                </div>
                <div class="history-controls">
                  <el-input
                    v-model="searchQuery"
                    placeholder="搜索消息内容..."
                    :prefix-icon="Search"
                    size="small"
                    class="search-input"
                  ></el-input>
                </div>
              </div>
            </template>

        <el-table
          v-if="filteredHistory.length > 0"
          v-loading="isLoadingHistory"
          :data="paginatedHistory"
          style="width: 100%"
          class="custom-table"
          border
          stripe
          :row-class-name="tableRowClassName"
          :show-empty="false"
        >
          <el-table-column prop="time" label="时间" width="180" sortable>
            <template #default="{ row }">
              <div class="time-cell">
                <div class="date">{{ formatDate(row.time) }}</div>
                <div class="time">{{ formatTime(row.time) }}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="originalMessage" label="原始消息" width="180">
            <template #default="{ row }">
              <el-tooltip :content="row.originalMessage" placement="top">
                <div class="message-content">{{ truncateText(row.originalMessage, 20) }}</div>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="aiReply" label="AI 回复">
            <template #default="{ row }">
              <el-tooltip :content="row.aiReply" placement="top">
                <div class="reply-cell">{{ truncateText(row.aiReply, 30) }}</div>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag
                :type="row.status === 'replied' ? 'success' : 'info'"
                size="small"
                class="status-tag"
              >
                {{ row.status === 'replied' ? '已回复' : '待回复' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <div class="operation-buttons">
                <el-button
                  type="primary"
                  size="small"
                  @click="viewDetails(row)"
                  :icon="View"
                >
                  查看
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-container" v-if="filteredHistory.length > 0">
          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="filteredHistory.length"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            class="custom-pagination"
          ></el-pagination>
        </div>

        <el-empty v-else-if="!isLoadingHistory" description="暂无回复历史" />
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { View, Search } from '@element-plus/icons-vue'


const aiForm = ref(null)
const rulesForm = ref(null)


const formData = reactive({
  aiStatus: false,
  replyDelay: 5,
  minReplyInterval: 60,
  replyTemplate: '感谢您的消息：{content}。此消息由AI自动回复，时间：{time}。',
  contactPerson: '',
  aiPersona: '我是一个友好、专业的AI助手，致力于为用户提供准确、及时的帮助。',
  customRules: [
    {
      id: 1,
      matchType: 'contains',
      keyword: '发货',
      reply: '我们的商品通常会在下单后1-3个工作日内发货。'
    },
    {
      id: 2,
      matchType: 'equals',
      keyword: '退款',
      reply: '您可以在订单详情页面申请退款，我们会在24小时内处理。'
    }
  ]
})


const startTime = ref(null)
const takeoverDuration = ref(0)
const timerInterval = ref(null)


const formattedTakeoverTime = computed(() => {
  const seconds = Math.floor(takeoverDuration.value / 1000)
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
})


const toggleTakeover = () => {
  if (formData.aiStatus) {
    formData.aiStatus = false
    clearInterval(timerInterval.value)
    timerInterval.value = null
    ElMessage.info('AI已停止接管消息回复')
  } else {
    formData.aiStatus = true
    startTime.value = Date.now()
    timerInterval.value = setInterval(() => {
      takeoverDuration.value = Date.now() - startTime.value
    }, 1000)
    ElMessage.success('AI已开始接管消息回复')
  }
}


onUnmounted(() => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
})

const rules = {
  replyDelay: [
    { required: true, message: '请输入回复延迟', trigger: 'blur' },
    { type: 'number', message: '回复延迟必须是数字', trigger: 'blur' },
    { min: 0, max: 30, message: '回复延迟必须在0-30秒之间', trigger: 'blur' }
  ],
  minReplyInterval: [
    { required: true, message: '请输入最小回复间隔时间', trigger: 'blur' },
    { type: 'number', message: '间隔时间必须是数字', trigger: 'blur' },
    { min: 0, max: 3600, message: '间隔时间必须在0-3600秒之间', trigger: 'blur' }
  ],
  contactPerson: [
    { required: true, message: '请输入接管联系人', trigger: 'blur' }
  ],
  aiPersona: [
    { required: true, message: '请输入AI人设', trigger: 'blur' },
    { min: 10, max: 500, message: 'AI人设长度必须在10-500个字符之间', trigger: 'blur' }
  ]
}


const addRule = () => {
  formData.customRules.push({
    id: Date.now(),
    matchType: 'contains',
    keyword: '',
    reply: ''
  })
}


const removeRule = (index) => {
  formData.customRules.splice(index, 1)
}


const replyHistory = ref([])


const searchQuery = ref('')
const filterStatus = ref('all')
const currentPage = ref(1)
const pageSize = ref(5)
const isLoadingHistory = ref(false)
const isSubmitting = ref(false)


const stats = reactive({
  replyRate: 95,
  averageTime: 2.8,
  satisfactionRate: 92
})


const filteredHistory = computed(() => {
  return replyHistory.value
    .filter(item => {
      const matchesSearch = item.originalMessage.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          item.aiReply.toLowerCase().includes(searchQuery.value.toLowerCase())
      const matchesStatus = filterStatus.value === 'all' || item.status === filterStatus.value
      return matchesSearch && matchesStatus
    })
})


const paginatedHistory = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value
  return filteredHistory.value.slice(startIndex, startIndex + pageSize.value)
})

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (current) => {
  currentPage.value = current
}


const submitForm = async () => {
  isSubmitting.value = true
  try {
    await aiForm.value.validate()
    await rulesForm.value.validate()

    const response = await fetch('/api/ai-settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })

    if (response.ok) {
      ElMessage.success('AI设置保存成功')
    } else {
      ElMessage.error('保存失败，请稍后重试')
    }
  } catch (error) {
    console.error('表单验证失败:', error)
    ElMessage.error('保存失败，请检查表单填写是否正确')
  } finally {
    isSubmitting.value = false
  }
}


const resetForm = () => {
  ElMessageBox.confirm('确定要重置所有设置吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    formData.aiStatus = false
    formData.replyDelay = 5
    formData.minReplyInterval = 60
    formData.contactPerson = ''
    formData.aiPersona = '我是一个友好、专业的AI助手，致力于为用户提供准确、及时的帮助。'
    formData.customRules = [
      {
        matchType: 'contains',
        keyword: '发货',
        reply: '我们的商品通常会在下单后1-3个工作日内发货。'
      },
      {
        matchType: 'equals',
        keyword: '退款',
        reply: '您可以在订单详情页面申请退款，我们会在24小时内处理。'
      }
    ]
    ElMessage.success('设置已重置')
  }).catch(() => {})
}


const viewDetails = (row) => {
  ElMessageBox({
    title: '消息详情',
    message: `
      <div class="detail-item">
        <div class="detail-label">时间:</div>
        <div class="detail-value">${row.time}</div>
      </div>
      <div class="detail-item">
        <div class="detail-label">原始消息:</div>
        <div class="detail-value">${row.originalMessage}</div>
      </div>
      <div class="detail-item">
        <div class="detail-label">AI回复:</div>
        <div class="detail-value">${row.aiReply || '暂无回复'}</div>
      </div>
      <div class="detail-item">
        <div class="detail-label">状态:</div>
        <div class="detail-value">${row.status === 'replied' ? '已回复' : '待回复'}</div>
      </div>
    `,
    dangerouslyUseHTMLString: true,
    confirmButtonText: '关闭'
  })
}


const formatDate = (dateTime) => {
  const date = new Date(dateTime)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const formatTime = (dateTime) => {
  const date = new Date(dateTime)
  return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}


const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? `${text.substring(0, length)}...` : text
}


const tableRowClassName = ({ row }) => {
  return row.status === 'pending' ? 'task-pending' : 'task-completed';
}

const animateCounters = () => {
  const counters = document.querySelectorAll('.counter');
  if (counters.length) {
    counters.forEach(counter => {
      
      counter.style.opacity = '0';
      counter.style.transform = 'translateY(20px)';
      counter.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

      
      setTimeout(() => {
        counter.style.opacity = '1';
        counter.style.transform = 'translateY(0)';

        const target = +counter.dataset.target;
        const duration = 2500;
        const frameDuration = 1000 / 60;
        const totalFrames = Math.round(duration / frameDuration);
        let frame = 0;

        
        const easeOutQuad = (t) => t * (2 - t);

        const updateCounter = () => {
          frame++;
          const progress = easeOutQuad(frame / totalFrames);
          const current = Math.round(target * progress);

          counter.innerText = current.toLocaleString();

          if ( frame < totalFrames) {
            requestAnimationFrame(updateCounter);
          } else {
            counter.innerText = target.toLocaleString();
          }
        };

        updateCounter();
      }, Math.random() * 300);
    });
  }
}

onMounted(() => {
  // 从API加载AI回复历史
  const fetchReplyHistory = async () => {
    isLoadingHistory.value = true
    try {
      const response = await fetch('/api/ai-history')
      if (response.ok) {
        const data = await response.json()
        replyHistory.value = data
      } else {
        ElMessage.error('获取回复历史失败')
      }
    } catch (error) {
      console.error('获取回复历史失败:', error)
      ElMessage.error('获取回复历史失败')
    } finally {
      isLoadingHistory.value = false
      // 加载完成后执行动画
      setTimeout(() => {
        animateCounters();
      }, 500);
    }
  }

  fetchReplyHistory()
});
</script>

<style scoped>
:root {
  --primary-color: #3b82f6;
  --primary-dark: #1d4ed8;
  --primary-light: #93c5fd;
  --secondary-color: #60a5fa;
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
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --transition: all 0.3s ease;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

/* 顶部导航 */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: white;
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 10;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  font-size: 18px;
  color: var(--primary-color);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

/* 页面标题区域 */
.page-header-section {
  margin-bottom: 24px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  padding: 32px 0;
  color: white;
}

.page-header {
  text-align: center;
  padding: 1rem 0;
}

.page-header h1 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  max-width: 700px;
  margin: 0 auto;
}

/* 主要内容区域 */
.main-content {
  padding: 0 24px 24px;
  max-width: 1600px;
  margin: 0 auto;
}

/* 上方左右排列区域 */
.top-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.config-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.config-card-inner {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 统一卡片头部样式 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
  background-color: white;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
  color: var(--text-primary);
}

/* 统一表单行间距 */
.el-row {
  margin-bottom: 20px;
}

/* 状态切换样式优化 */
.status-controls {
  display: flex;
  align-items: center;
}

.takeover-time {
  font-size: 14px;
  color: var(--text-secondary);
}

.takeover-time.text-primary {
  color: var(--primary-color);
  font-weight: 500;
}

/* 统一统计卡片样式 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
  margin: 16px 0;
}

.stat-item {
  padding: 16px;
  border-radius: 12px;
  background-color: white;
  box-shadow: var(--shadow);
  text-align: center;
  transition: var(--transition);
  border: 1px solid var(--border-color);
}

.stat-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

/* 图表样式 */
.chart-card {
  background-color: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-actions {
  display: flex;
  gap: 8px;
}

.chart-select {
  width: 100px;
}

/* 统一表格操作按钮 */
.el-table .el-button {
  margin: 0 4px;
  padding: 4px 8px;
  font-size: 12px;
}

/* 自定义输入框样式 */
.custom-input .el-input__wrapper {
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.custom-input .el-input__wrapper:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

/* 自定义选择框样式 */
.custom-select .el-input__wrapper {
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

/* 按钮样式增强 - 与AutoInfoView统一 */
/* 移除渐变按钮样式，使用标准按钮样式 */
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
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(30, 64, 175, 0.2);
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

.delete-btn {
  background-color: #fee2e2;
  border-color: #fecaca;
  color: #dc2626;
  transition: all 0.2s ease;
}

.delete-btn:hover {
  background-color: #fecaca;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
}

/* 卡片样式 */
.el-card {
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  overflow: hidden;
  background-color: white;
  margin-bottom: 24px;
}

.el-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  border-color: var(--primary-light);
}

/* 卡片相关样式已与AutoInfoView统一 */

/* 移除了.card-icon、.card-title-group、.card-title和.card-subtitle类，使用.header-title替代 */

/* 表单样式 */
.el-form-item {
  margin-bottom: 24px;
}

.status-toggle {
  display: flex;
  align-items: center;
}

.status-toggle .el-form-item__content {
  flex: 1;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
  padding: 5px 0;
}

/* 表格样式增强 - 与AutoInfoView统一 */
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
  background-color: var(--light-color);
}

/* 标签样式 */
.el-tag--info {
  background-color: rgba(59, 130, 246, 0.1);
  color: var(--secondary-color);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 6px;
}

.el-tag--success {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 6px;
}

/* 分页样式 */
.custom-pagination {
  padding: 16px 0;
  display: flex;
  justify-content: flex-end;
}

/* 自定义规则样式 */
.custom-rules-container {
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 15px;
  background-color: white;
}

.rule-actions {
  margin-bottom: 16px;
}

.rules-table {
  margin-top: 15px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .top-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .page-header h1 {
    font-size: 1.8rem;
  }

  .logo span {
    display: none;
  }
}
</style>