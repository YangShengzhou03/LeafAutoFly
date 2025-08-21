<template>
  <div class="home-container">

    <section class="pricing">
      <div class="section-header">
        <h2>选择适合您企业的方案</h2>
        <p>灵活的定价策略，满足不同规模企业的需求</p>
      </div>
      <div class="pricing-cards">
        <template v-for="plan in homeData.pricingPlans" :key="plan.id">
          <div :class="['pricing-card', { 'popular': plan.isPopular }]">
            <div v-if="plan.isPopular" class="popular-tag">最受欢迎</div>
            <div class="card-header">
              <h3>{{ plan.name }}</h3>
              <div class="price">
                <span class="amount">{{ typeof plan.price === 'number' ? '¥' + plan.price : plan.price }}</span>
                <span class="period">{{ plan.period }}</span>
              </div>
            </div>
            <div class="card-features">
              <div class="feature" v-for="feature in plan.features" :key="feature">
                <i class="el-icon-check"></i>
                <span>{{ feature }}</span>
              </div>
            </div>
            <button :class="['select-plan', { 'popular-btn': plan.isPopular }]">
              {{ plan.isPopular ? '选择方案' : (plan.id === 3 ? '联系我们' : '选择方案') }}
            </button>
          </div>
        </template>
      </div>
    </section>


    <section class="key-metrics">
      <div class="metrics-container">
        <div class="metric-card" v-for="metric in homeData.keyMetrics" :key="metric.id">
          <div class="metric-value counter" :data-target="metric.value">{{ metric.value }}</div>
          <div class="metric-label">{{ metric.label }}</div>
        </div>
      </div>
    </section>


    <section class="dashboard">
      <div class="section-header">
        <h2>系统概览</h2>
        <p>实时监控您的自动化状态和效果</p>
      </div>
      <div class="dashboard-cards">
        <div class="dashboard-card" v-for="item in homeData.dashboardData" :key="item.id">
          <div class="card-title">
            <h3>{{ item.title }}</h3>
            <span v-if="item.trend" :class="item.trend === 'up' ? 'trend-up' : 'trend-down'">
              <i :class="item.trend === 'up' ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i> {{ item.trendValue }}%
            </span>
          </div>
          <div :class="['card-value', { 'status-normal': item.status === 'normal' }]">
            {{ item.value }}{{ item.id !== 4 ? '%' : '' }}
          </div>
          <div class="card-footer">
            <span>{{ item.footer }}</span>
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
        <div class="testimonial-card" v-for="testimonial in homeData.testimonials" :key="testimonial.id">
          <div class="quote">"{{ testimonial.quote }}"</div>
          <div class="customer-info">
            <img :src="require('@/assets/images/user-avatar.svg')" alt="客户头像"
              class="w-12 h-12 rounded-full object-cover mr-4 bg-gray-100" />
            <div class="customer-details">
              <div class="name">{{ testimonial.customerName }}</div>
              <div class="company">{{ testimonial.customerCompany }}</div>
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
const homeData = ref({
  pricingPlans: [],
  keyMetrics: [],
  dashboardData: [],
  testimonials: []
});

// 从后端获取数据
const fetchHomeData = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/home-data');
    const data = await response.json();
    homeData.value = data;

    // 数据加载完成后触发动画
    if (!animationActive.value) {
      triggerAnimations();
    }
  } catch (error) {
    console.error('获取首页数据失败:', error);
  }
};

// 触发动画的函数
const triggerAnimations = () => {
  animationActive.value = true;
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
};

onMounted(() => {
  fetchHomeData();
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