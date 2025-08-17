<template>
  <div class="home-container">
    <!-- 会员套餐卡片区域 -->
    <div class="membership-cards">
      <div class="membership-card free-card">
        <div class="card-tag">免费</div>
        <div class="card-title">免费版（beta 中）</div>
        <div class="card-subtitle">有效期至 2025-09-12</div>
        <div class="card-features">
          <div class="feature">基础功能</div>
          <div class="feature">每日限量</div>
        </div>
        <button class="card-button free-button">继续使用</button>
      </div>
      
      <div class="membership-card monthly-card">
        <div class="card-tag">限时优惠</div>
        <div class="card-title">月度会员</div>
        <div class="card-subtitle">¥29.9 / 月</div>
        <div class="card-features">
          <div class="feature">全部功能</div>
          <div class="feature">优先支持</div>
        </div>
        <button class="card-button monthly-button">立即订阅</button>
      </div>
      
      <div class="membership-card quarterly-card">
        <div class="card-tag">限时优惠</div>
        <div class="card-title">季度会员</div>
        <div class="card-subtitle">¥269.9 / 季</div>
        <div class="card-discount">省 ¥9.8</div>
        <div class="card-features">
          <div class="feature">全部功能</div>
          <div class="feature">数据导出</div>
        </div>
        <button class="card-button quarterly-button">立即订阅</button>
      </div>
      
      <div class="membership-card yearly-card">
        <div class="card-tag">年度</div>
        <div class="card-title">年度会员</div>
        <div class="card-subtitle">¥899 / 年</div>
        <div class="card-discount">省 ¥338.8</div>
        <div class="card-features">
          <div class="feature">全部功能</div>
          <div class="feature">专属客服</div>
        </div>
        <button class="card-button yearly-button">立即订阅</button>
      </div>
    </div>
    
    <!-- 数据统计卡片区域 -->
    <div class="stat-cards">
      <div class="stat-card">
        <div class="stat-icon purple-icon">
          <i class="el-icon-line-chart"></i>
        </div>
        <div class="stat-title">自动化能力</div>
        <div class="stat-desc"><span class="stat-value">12%</span> 当前自动化任务完成率</div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon purple-icon">
          <i class="el-icon-coffee-cup"></i>
        </div>
        <div class="stat-title">AI 能力</div>
        <div class="stat-desc"><span class="stat-value">6%</span> AI 辅助功能使用率</div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon purple-icon">
          <i class="el-icon-check"></i>
        </div>
        <div class="stat-title">系统状态</div>
        <div class="stat-desc"><span class="status-normal">正常运行</span> 无异常，运行稳定</div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon purple-icon">
          <i class="el-icon-sun"></i>
        </div>
        <div class="stat-title">更新状态</div>
        <div class="stat-desc"><span class="status-latest">已是最新版本</span> 版本号: v1.0.0</div>
      </div>
    </div>
    
    <!-- 欢迎信息区域 -->
    <div class="welcome-section">
      <div class="welcome-decoration"></div>
      <div class="welcome-title">欢迎使用 LeafAuto Web</div>
      <div class="welcome-desc">LeafAuto 是我在 2024 年大二时写的练习程序，主要用于自动化微信消息发送和管理。</div>
      
      <div class="welcome-stats">
        <div class="welcome-stat">
          <div class="stat-number">500+</div>
          <div class="stat-label">活跃用户</div>
        </div>
        
        <div class="welcome-stat">
          <div class="stat-number">10k+</div>
          <div class="stat-label">自动化任务</div>
        </div>
        
        <div class="welcome-stat">
          <div class="stat-number">98%</div>
          <div class="stat-label">系统稳定性</div>
        </div>
      </div>
      
      <div class="welcome-thanks">感谢您的使用和支持！</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 添加统计卡片图标动画效果
onMounted(() => {
  const statIcons = document.querySelectorAll('.stat-icon');
  statIcons.forEach(icon => {
    icon.addEventListener('mouseenter', () => {
      icon.classList.add('shake');
    });
    icon.addEventListener('mouseleave', () => {
      icon.classList.remove('shake');
    });
  });

  // 添加会员卡片按钮hover效果
  const cardButtons = document.querySelectorAll('.card-button');
  cardButtons.forEach(button => {
    button.addEventListener('mouseenter', () => {
      button.classList.add('hover');
    });
    button.addEventListener('mouseleave', () => {
      button.classList.remove('hover');
    });
  });
});
</script>

<style scoped>
.home-container {
  padding: 24px;
  box-sizing: border-box;
}

/* 会员套餐卡片区域样式 */
.membership-cards {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 24px;
}

.membership-card {
  flex: 1;
  padding: 24px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  position: relative;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s, box-shadow 0.3s;
}

.membership-card:hover {
  transform: translateY(-5px);
}

.free-card {
  background: linear-gradient(135deg, rgba(233, 213, 255, 0.8), rgba(251, 233, 255, 0.8));
  box-shadow: 0 4px 15px rgba(216, 180, 254, 0.2);
}

.monthly-card {
  background: linear-gradient(135deg, rgba(219, 234, 254, 0.8), rgba(216, 240, 254, 0.8));
  box-shadow: 0 4px 15px rgba(191, 219, 254, 0.2);
}

.quarterly-card {
  background: linear-gradient(135deg, rgba(216, 240, 254, 0.8), rgba(217, 249, 235, 0.8));
  box-shadow: 0 4px 15px rgba(191, 242, 219, 0.2);
}

.yearly-card {
  background: linear-gradient(135deg, rgba(254, 236, 217, 0.8), rgba(254, 243, 199, 0.8));
  box-shadow: 0 4px 15px rgba(252, 231, 178, 0.2);
}

.card-tag {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 4px 12px;
  border-radius: 20px;
  border: 1px solid #d0d3d9;
  background-color: white;
  color: #666;
  font-size: 12px;
}

.monthly-card .card-tag, .quarterly-card .card-tag {
  left: auto;
  right: 16px;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
  margin-top: 40px;
}

.card-subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 16px;
}

.card-discount {
  font-size: 14px;
  color: #10b981;
  margin-bottom: 16px;
}

.card-features {
  margin-bottom: 24px;
  flex-grow: 1;
}

.feature {
  margin-bottom: 8px;
  color: #666;
  font-size: 14px;
}

.card-button {
  padding: 10px 0;
  border-radius: 8px;
  border: none;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.card-button.hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.free-button {
  background: linear-gradient(to right, #9333ea, #c084fc);
}

.monthly-button {
  background: linear-gradient(to right, #3b82f6, #60a5fa);
}

.quarterly-button {
  background: linear-gradient(to right, #14b8a6, #2dd4bf);
}

.yearly-button {
  background: linear-gradient(to right, #f97316, #fb923c);
}

/* 数据统计卡片区域样式 */
.stat-cards {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 24px;
}

.stat-card {
  flex: 1;
  padding: 24px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  font-size: 24px;
  color: white;
  transition: all 0.3s;
}

.purple-icon {
  background: linear-gradient(135deg, #9333ea, #c084fc);
}

.shake {
  animation: shake 0.5s;
}

@keyframes shake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-5deg); }
  75% { transform: rotate(5deg); }
}

.stat-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.stat-desc {
  font-size: 14px;
  color: #666;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #9333ea;
}

.status-normal {
  color: #10b981;
  font-weight: bold;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: rgba(16, 185, 129, 0.1);
}

.status-latest {
  color: #3b82f6;
  font-weight: bold;
  padding: 2px 8px;
  border-radius: 4px;
  background-color: rgba(59, 130, 246, 0.1);
}

/* 欢迎信息区域样式 */
.welcome-section {
  padding: 32px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

.welcome-decoration {
  width: 80px;
  height: 2px;
  background: linear-gradient(to right, #9333ea, transparent);
  margin-bottom: 16px;
}

.welcome-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
}

.welcome-desc {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 24px;
}

.welcome-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 24px;
}

.welcome-stat {
  flex: 1;
  padding: 16px;
  background-color: white;
  border-radius: 8px;
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.03);
  text-align: center;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #9333ea;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.welcome-thanks {
  text-align: center;
  font-size: 16px;
  color: #666;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  position: relative;
}

.welcome-thanks::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 2px;
  background: linear-gradient(to right, #9333ea, transparent);
}
</style>