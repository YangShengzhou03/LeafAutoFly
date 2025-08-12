<template>
  <div class="task-detail-container">
    <el-card class="task-card">
      <div class="task-header">
        <h2 class="task-title">{{ task.title }}</h2>
        <div class="task-actions">
          <el-button type="primary" size="small" @click="handleEdit">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete" style="margin-left: 10px;">删除</el-button>
        </div>
      </div>

      <div class="task-meta">
        <div class="meta-item">
          <span class="meta-label">任务ID:</span>
          <span class="meta-value">{{ task.id }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">状态:</span>
          <el-tag :type="getStatusTagType(task.status)">{{ getStatusText(task.status) }}</el-tag>
        </div>
        <div class="meta-item">
          <span class="meta-label">优先级:</span>
          <el-tag :type="getPriorityTagType(task.priority)" size="small">{{ getPriorityText(task.priority) }}</el-tag>
        </div>
        <div class="meta-item">
          <span class="meta-label">创建时间:</span>
          <span class="meta-value">{{ task.createTime }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">截止时间:</span>
          <span class="meta-value">{{ task.dueTime }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">负责人:</span>
          <span class="meta-value">{{ task.assignee }}</span>
        </div>
      </div>

      <div class="task-description">
        <h3>任务描述</h3>
        <p>{{ task.description }}</p>
      </div>

      <div class="task-progress">
        <h3>任务进度</h3>
        <el-progress :percentage="task.progress || 0"></el-progress>
      </div>

      <div class="task-comments" v-if="task.comments && task.comments.length > 0">
        <h3>评论</h3>
        <div class="comment-list">
          <div class="comment-item" v-for="comment in task.comments" :key="comment.id">
            <div class="comment-header">
              <span class="comment-author">{{ comment.author }}</span>
              <span class="comment-time">{{ comment.time }}</span>
            </div>
            <div class="comment-content">{{ comment.content }}</div>
          </div>
        </div>
      </div>

      <div class="add-comment" v-if="showAddComment">
        <el-input
          type="textarea"
          v-model="newComment"
          placeholder="添加评论..."
          rows="3"
        ></el-input>
        <el-button type="primary" size="small" @click="submitComment" style="margin-top: 10px;">提交</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Edit, Delete, Message as MessageIcon }
  from '@element-plus/icons-vue'

// 响应式数据
const task = ref({})
const newComment = ref('')
const showAddComment = ref(true)
const route = useRoute()
const router = useRouter()
const taskId = route.params.id

// 生命周期钩子
onMounted(() => {
  fetchTaskDetail()
})

// 模拟获取任务详情
const fetchTaskDetail = () => {
  // 模拟API请求
  setTimeout(() => {
    // 这里应该是从API获取的数据
    task.value = {
      id: taskId,
      title: '系统优化',
      description: '对系统性能进行全面优化，包括前端渲染速度和后端响应时间。重点关注大数据量下的性能表现。',
      status: 'in_progress',
      priority: 'high',
      createTime: '2023-11-10 10:00:00',
      dueTime: '2023-11-20 18:00:00',
      assignee: '张三',
      progress: 60,
      comments: [
        {
          id: 1,
          author: '张三',
          time: '2023-11-12 14:30:00',
          content: '已经完成了前端部分的优化，现在开始处理后端。'
        },
        {
          id: 2,
          author: '李四',
          time: '2023-11-13 09:15:00',
          content: '建议关注数据库查询性能，这部分可能是瓶颈。'
        }
      ]
    }
  }, 500)
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    pending: '待处理',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

// 获取状态标签类型
const getStatusTagType = (status) => {
  const typeMap = {
    pending: 'warning',
    in_progress: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return typeMap[status] || 'default'
}

// 获取优先级文本
const getPriorityText = (priority) => {
  const priorityMap = {
    high: '高',
    medium: '中',
    low: '低'
  }
  return priorityMap[priority] || priority
}

// 获取优先级标签类型
const getPriorityTagType = (priority) => {
  const typeMap = {
    high: 'danger',
    medium: 'warning',
    low: 'success'
  }
  return typeMap[priority] || 'default'
}

// 处理编辑按钮点击
const handleEdit = () => {
  router.push(`/task/edit/${task.value.id}`)
}

// 处理删除按钮点击
const handleDelete = () => {
  ElMessage.confirm('确定要删除该任务吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 模拟删除操作
    setTimeout(() => {
      ElMessage.success('任务删除成功')
      router.push('/task/list')
    }, 500)
  })
}

// 提交评论
const submitComment = () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  // 模拟提交评论
  setTimeout(() => {
    const newCommentObj = {
      id: Date.now(),
      author: '当前用户',
      time: new Date().toLocaleString(),
      content: newComment.value
    }

    if (!task.value.comments) {
      task.value.comments = []
    }

    task.value.comments.push(newCommentObj)
    newComment.value = ''
    ElMessage.success('评论添加成功')
  }, 500)
}
</script>

<style scoped>
.task-detail-container {
  padding: 20px;
}

.task-card {
  margin-bottom: 20px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.task-title {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}

.task-actions {
  display: flex;
}

.task-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px 30px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-label {
  width: 80px;
  color: #666;
}

.meta-value {
  flex: 1;
}

.task-description,
.task-progress,
.task-comments {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.task-description h3,
.task-progress h3,
.task-comments h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: bold;
}

.comment-list {
  margin-top: 15px;
}

.comment-item {
  padding: 10px 0;
  border-bottom: 1px solid #f5f5f5;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.comment-author {
  font-weight: bold;
}

.comment-time {
  color: #999;
  font-size: 12px;
}

.comment-content {
  color: #333;
}

.add-comment {
  margin-top: 20px;
}
</style>