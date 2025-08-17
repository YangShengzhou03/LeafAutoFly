<template>
  <div class="home-container">
    <!-- 会员卡片区域 -->
    <div class="membership-cards">
      <div class="membership-card purple-card">
        <div class="card-title">充值版</div>
        <div class="card-subtitle">有效期至: 2025-09-12</div>
        <div class="card-features">
          <div class="feature">• 基础版</div>
          <div class="feature">• 每周限</div>
        </div>
        <el-button class="card-button" type="primary" size="small">查看详情</el-button>
      </div>
      
      <div class="membership-card blue-card">
        <div class="card-title">月度会员</div>
        <div class="card-subtitle">¥28.00/月</div>
        <div class="card-features">
          <div class="feature">• 基础版</div>
          <div class="feature">• 优先处理</div>
          <div class="feature">• 优惠券</div>
        </div>
        <el-button class="card-button" type="primary" size="small">立即订阅</el-button>
      </div>
      
      <div class="membership-card green-card">
        <div class="card-title">季度会员</div>
        <div class="card-subtitle">¥68.00/季</div>
        <div class="card-features">
          <div class="feature">• 专业版</div>
          <div class="feature">• 无限制</div>
          <div class="feature">• 高级支持</div>
        </div>
        <el-button class="card-button" type="primary" size="small">立即订阅</el-button>
      </div>
      
      <div class="membership-card orange-card">
        <div class="card-title">年度会员</div>
        <div class="card-subtitle">¥198.00/年</div>
        <div class="card-features">
          <div class="feature">• 企业版</div>
          <div class="feature">• 专属功能</div>
          <div class="feature">• 专属客服</div>
        </div>
        <el-button class="card-button" type="primary" size="small">立即订阅</el-button>
      </div>
    </div>
    
    <!-- 功能卡片区域 -->
    <div class="feature-cards">
      <div class="feature-card">
        <div class="feature-icon">
          <i class="el-icon-s-promotion"></i>
        </div>
        <div class="feature-title">API接口</div>
        <div class="feature-desc">标准化的API接口文档</div>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">
          <i class="el-icon-s-robot"></i>
        </div>
        <div class="feature-title">AI能力</div>
        <div class="feature-desc">AI辅助内容生成系统</div>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">
          <i class="el-icon-s-timer"></i>
        </div>
        <div class="feature-title">定时任务</div>
        <div class="feature-desc">支持每日、每周、每月定时</div>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">
          <i class="el-icon-s-check"></i>
        </div>
        <div class="feature-title">版本检查</div>
        <div class="feature-desc">当前版本: v1.0.0</div>
      </div>
    </div>
    
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-title">欢迎使用 LeafAuto Web</div>
      <div class="welcome-desc">LeafAuto 是2024年人工智能学习项目，主要用于自动化信息发送及管理。</div>
      
      <div class="welcome-stats">
        <div class="welcome-stat">
          <div class="stat-number">500+</div>
          <div class="stat-label">成功发送的信息</div>
        </div>
        
        <div class="welcome-stat">
          <div class="stat-number">10k+</div>
          <div class="stat-label">满意用户</div>
        </div>
        
        <div class="welcome-stat">
          <div class="stat-number">99%</div>
          <div class="stat-label">系统稳定性</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElButton } from 'element-plus'

const router = useRouter()

// 导航到自动信息页面
function navigateToAutoInfo() {
  router.push('/auto_info')
}

// 导航到AI接管页面
function navigateToAITakeover() {
  router.push('/ai_takeover')
}
</script>

<style scoped>
:root {
  --primary-color: #1890ff;
  --purple-color: #722ed1;
  --blue-color: #1e88e5;
  --green-color: #388e3c;
  --orange-color: #ff7043;
  --shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  --shadow-hover: 0 8px 20px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}

.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 会员卡片样式 */
.membership-cards {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}

.membership-card {
  flex: 1;
  min-width: 250px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--shadow);
  color: white;
  position: relative;
  overflow: hidden;
  transition: var(--transition);
}

.membership-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}

.purple-card {
  background: linear-gradient(135deg, #9c27b0 0%, #722ed1 100%);
}

.blue-card {
  background: linear-gradient(135deg, #2196f3 0%, #1e88e5 100%);
}

.green-card {
  background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
}

.orange-card {
  background: linear-gradient(135deg, #ff9800 0%, #ff7043 100%);
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.card-subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 15px;
}

.card-features {
  margin-bottom: 20px;
}

.feature {
  font-size: 13px;
  margin-bottom: 5px;
  opacity: 0.9;
}

.card-button {
  width: 100%;
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
  color: white;
}

.card-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.6);
  color: white;
}

/* 功能卡片样式 */
.feature-cards {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}

.feature-card {
  flex: 1;
  min-width: 200px;
  padding: 25px 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: var(--shadow);
  text-align: center;
  transition: var(--transition);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
}

.feature-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 15px;
  background-color: #f0f7ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: var(--primary-color);
}

.feature-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.feature-desc {
  font-size: 14px;
  color: #666;
}

/* 欢迎区域样式 */
.welcome-section {
  background-color: white;
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 30px;
  text-align: center;
}

.welcome-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

.welcome-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 25px;
}

.welcome-stats {
  display: flex;
  justify-content: center;
  gap: 50px;
}

.welcome-stat {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}
</style>