<template>
  <div class="home-container">
    
    <section class="pricing">
      <div class="section-header">
        <h2>选择适合您企业的方案</h2>
        <p>灵活的定价策略，满足不同规模企业的需求</p>
      </div>
      <div class="pricing-cards">
        <div class="pricing-card">
          <div class="card-header">
            <h3>基础版</h3>
            <div class="price">
              <span class="amount">¥299</span>
              <span class="period">/年</span>
            </div>
          </div>
          <div class="card-features">
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>基础消息发送功能</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>每日1000条发送限额</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>无数据分析功能</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>邮件支持</span>
            </div>
          </div>
          <button class="select-plan">选择方案</button>
        </div>

        <div class="pricing-card popular">
          <div class="popular-tag">最受欢迎</div>
          <div class="card-header">
            <h3>企业版</h3>
            <div class="price">
              <span class="amount">¥899</span>
              <span class="period">/年</span>
            </div>
          </div>
          <div class="card-features">
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>无限制消息发送</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>高级数据分析与报表</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>客户画像分析</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>优先技术支持</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>API访问权限</span>
            </div>
          </div>
          <button class="select-plan popular-btn">选择方案</button>
        </div>

        <div class="pricing-card">
          <div class="card-header">
            <h3>定制版</h3>
            <div class="price">
              <span class="amount">联系我们</span>
              <span class="period">获取报价</span>
            </div>
          </div>
          <div class="card-features">
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>完全定制化功能</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>专属客户经理</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>私有部署选项</span>
            </div>
            <div class="feature">
              <i class="el-icon-check"></i>
              <span>24/7技术支持</span>
            </div>
          </div>
          <button class="select-plan">联系我们</button>
        </div>
      </div>
    </section>

        
    <section class="key-metrics">
      <div class="metrics-container">
        <div class="metric-card">
          <div class="metric-value counter" data-target="500">0</div>
          <div class="metric-label">活跃企业客户</div>
        </div>
        <div class="metric-card">
          <div class="metric-value counter" data-target="10000">0</div>
          <div class="metric-label">自动化任务</div>
        </div>
        <div class="metric-card">
          <div class="metric-value counter" data-target="98">0</div>
          <div class="metric-label">系统稳定性</div>
        </div>
        <div class="metric-card">
          <div class="metric-value counter" data-target="1000000">0</div>
          <div class="metric-label">消息发送量</div>
        </div>
      </div>
    </section>

    
    <section class="dashboard">
      <div class="section-header">
        <h2>系统概览</h2>
        <p>实时监控您的自动化状态和效果</p>
      </div>
      <div class="dashboard-cards">
        <div class="dashboard-card">
          <div class="card-title">
            <h3>自动化任务完成率</h3>
            <span class="trend-up"><i class="el-icon-arrow-up"></i> 3.2%</span>
          </div>
          <div class="card-value">12%</div>
          <div class="card-footer">
            <span>较昨日</span>
          </div>
        </div>

        <div class="dashboard-card">
          <div class="card-title">
            <h3>消息送达率</h3>
            <span class="trend-up"><i class="el-icon-arrow-up"></i> 1.8%</span>
          </div>
          <div class="card-value">97.5%</div>
          <div class="card-footer">
            <span>较昨日</span>
          </div>
        </div>

        <div class="dashboard-card">
          <div class="card-title">
            <h3>AI辅助功能使用率</h3>
            <span class="trend-down"><i class="el-icon-arrow-down"></i> 0.5%</span>
          </div>
          <div class="card-value">6%</div>
          <div class="card-footer">
            <span>较昨日</span>
          </div>
        </div>

        <div class="dashboard-card">
          <div class="card-title">
            <h3>系统状态</h3>
          </div>
          <div class="card-value status-normal">正常运行</div>
          <div class="card-footer">
            <span>版本: v1.0.0</span>
          </div>
        </div>
      </div>
    </section>

    
    <section class="testimonials">
      <div class="section-header">
        <h2>客户评价</h2>
        <p>听听我们的客户怎么说</p>
      </div>
      <div class="testimonial-cards">
        <div class="testimonial-card">
          <div class="quote">"LeafAuto帮助我们公司节省了大量的人力成本，消息发送效率提升了60%以上。"</div>
          <div class="customer-info">
            <img src="@/assets/images/user-avatar.svg" alt="客户头像" class="w-12 h-12 rounded-full object-cover mr-4 bg-gray-100" />
            <div class="customer-details">
              <div class="name">张三</div>
              <div class="company">某科技公司市场总监</div>
            </div>
          </div>
        </div>

        <div class="testimonial-card">
          <div class="quote">"数据分析功能非常强大，让我们能够精准了解客户需求，提升转化率。"</div>
          <div class="customer-info">
            <img src="@/assets/images/user-avatar.svg" alt="客户头像" class="w-12 h-12 rounded-full object-cover mr-4 bg-gray-100" />
            <div class="customer-details">
              <div class="name">李四</div>
              <div class="company">某电商平台运营主管</div>
            </div>
          </div>
        </div>

        <div class="testimonial-card">
          <div class="quote">"系统稳定性非常好，从未出现过 downtime，客服响应也非常及时。"</div>
          <div class="customer-info">
            <img src="@/assets/images/user-avatar.svg" alt="客户头像" class="w-12 h-12 rounded-full object-cover mr-4 bg-gray-100" />
            <div class="customer-details">
              <div class="name">王五</div>
              <div class="company">某金融机构IT负责人</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

const animationActive = ref(false);

onMounted(() => {
  const counters = document.querySelectorAll('.counter');
  if (counters.length && !animationActive.value) {
    animationActive.value = true;
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

          if (frame < totalFrames) {
            requestAnimationFrame(updateCounter);
          } else {
            counter.innerText = target.toLocaleString();
          }
        };

        updateCounter();
      }, Math.random() * 300);
    });
  }

  setTimeout(() => {
    document.querySelectorAll('.pricing-card, .dashboard-card, .testimonial-card, .metric-card').forEach((el, index) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';

      setTimeout(() => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }, index * 100 + Math.random() * 100);
    });
  }, 100);
});
</script>

<style>
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

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.home-container {
  background-color: var(--light-color);
  min-height: 100vh;
  overflow-x: hidden;
}

/* 核心数据区域 */
.key-metrics {
  background-color: var(--primary-color);
  color: white;
  padding: 3rem 5%;
}

.metrics-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 2rem;
}

.metric-card {
  flex: 1;
  min-width: 150px;
  text-align: center;
  padding: 1.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  backdrop-filter: blur(5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.metric-card:hover {
  transform: translateY(-5px);
  background-color: rgba(255, 255, 255, 0.15);
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.metric-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

/* 通用区域标题 */
.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
}

.section-header p {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 700px;
  margin: 0 auto;
}

/* 会员计划区域 */
.pricing {
  padding: 2rem 2%;
  background-color: white;
}

.pricing-cards {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.pricing-card {
  flex: 1;
  min-width: 280px;
  max-width: 350px;
  background-color: white;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 2rem;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.03);
}

.pricing-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 15px 30px rgba(30, 64, 175, 0.1);
  border-color: var(--primary-color);
}

.pricing-card.popular:hover {
  transform: translateY(-15px) scale(1.03);
}

.pricing-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.pricing-card.popular {
  border-color: var(--primary-color);
  transform: translateY(-10px);
  box-shadow: 0 10px 30px rgba(30, 64, 175, 0.1);
}

.popular-tag {
  position: absolute;
  top: 0;
  right: 0;
  background-color: var(--primary-color);
  color: white;
  padding: 0.25rem 1.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  transform: rotate(45deg) translate(35%, -100%);
  transform-origin: top right;
}

.card-header {
  margin-bottom: 2rem;
}

.card-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.price {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.amount {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
}

.period {
  color: var(--text-secondary);
}

.card-features {
  margin-bottom: 2rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.feature i {
  color: var(--success-color);
}

.feature span {
  color: var(--text-secondary);
}

.select-plan {
  width: 100%;
  padding: 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: white;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.select-plan:hover {
  background-color: rgba(30, 64, 175, 0.05);
}

.select-plan.popular-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
}

.select-plan.popular-btn:hover {
  background-color: #1e3a8a;
}

/* 系统概览区域 */
.dashboard {
  padding: 5rem 5%;
  background-color: #f1f5f9;
}

.dashboard-cards {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.dashboard-card {
  flex: 1;
  min-width: 250px;
  max-width: 300px;
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.07);
}

.card-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-title h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.trend-up {
  color: var(--success-color);
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.trend-down {
  color: var(--danger-color);
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.card-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.status-normal {
  color: var(--success-color);
  font-size: 1.8rem;
}

.card-footer {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* 客户评价区域 */
.testimonials {
  padding: 5rem 5%;
  background-color: white;
}

.testimonial-cards {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
  position: relative;
}

/* 轮播控制按钮 - 仅在移动设备上显示 */
.testimonial-controls {
  display: none;
}

@media (max-width: 768px) {
  .testimonial-cards {
    flex-wrap: nowrap;
    overflow-x: auto;
    padding: 1rem 0;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .testimonial-cards::-webkit-scrollbar {
    display: none;
  }

  .testimonial-card {
    flex: 0 0 90%;
    margin: 0 0.5rem;
    scroll-snap-align: center;
  }

  .testimonial-controls {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
  }

  .testimonial-control {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: var(--border-color);
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .testimonial-control.active {
    background-color: var(--primary-color);
    transform: scale(1.2);
  }
}

.testimonial-card {
  flex: 1;
  min-width: 300px;
  max-width: 400px;
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.07);
}

.quote {
  font-size: 1.1rem;
  color: var(--text-primary);
  margin-bottom: 2rem;
  line-height: 1.6;
  position: relative;
  padding-left: 1.5rem;
}

.quote::before {
  content: '"';
  position: absolute;
  top: 0;
  left: 0;
  font-size: 3rem;
  color: var(--primary-color);
  opacity: 0.2;
  line-height: 1;
}

.customer-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.customer-info img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.customer-details {
  display: flex;
  flex-direction: column;
}

.name {
  font-weight: 600;
  color: var(--text-primary);
}

.company {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* 响应式设计 - 只保留实际使用的元素的响应式样式 */
@media (max-width: 768px) {
  .metrics-container {
    flex-direction: column;
    align-items: center;
  }

  .metric-card {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 576px) {
  .pricing-card,
  .dashboard-card,
  .testimonial-card {
    max-width: 100%;
  }

  .section-header h2 {
    font-size: 1.5rem;
  }

  .section-header p {
    font-size: 1rem;
  }
}
</style>