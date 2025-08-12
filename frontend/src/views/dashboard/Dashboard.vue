<template>
  <div class="dashboard-container">
    <el-card shadow="hover" class="welcome-card">
      <div class="welcome-content">
        <h1>欢迎使用 LeafAuto 智能管理系统</h1>
        <p>这是一个基于 Vue3 和 Element Plus 的现代化前端界面</p>
        <el-button type="primary" size="large" @click="navigateToTasks">
          开始使用
        </el-button>
      </div>
    </el-card>

    <div class="stats-container">
      <el-card shadow="hover" class="stat-card">
        <div class="stat-content">
          <div class="stat-title">总任务数</div>
          <div class="stat-value">{{ totalTasks }}</div>
          <div class="stat-change"><span class="increase">+12%</span> 较上月</div>
        </div>
        <div class="stat-icon"><List /></div>
      </el-card>

      <el-card shadow="hover" class="stat-card">
        <div class="stat-content">
          <div class="stat-title">已完成任务</div>
          <div class="stat-value">{{ completedTasks }}</div>
          <div class="stat-change"><span class="increase">+8%</span> 较上月</div>
        </div>
        <div class="stat-icon"><Check /></div>
      </el-card>

      <el-card shadow="hover" class="stat-card">
        <div class="stat-content">
          <div class="stat-title">待处理任务</div>
          <div class="stat-value">{{ pendingTasks }}</div>
          <div class="stat-change"><span class="decrease">-5%</span> 较上月</div>
        </div>
        <div class="stat-icon"><Clock /></div>
      </el-card>

      <el-card shadow="hover" class="stat-card">
        <div class="stat-content">
          <div class="stat-title">AI 服务调用</div>
          <div class="stat-value">{{ aiCalls }}</div>
          <div class="stat-change"><span class="increase">+25%</span> 较上月</div>
        </div>
        <div class="stat-icon"><Cpu /></div>
      </el-card>
    </div>

    <div class="charts-container">
      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>任务完成趋势</span>
            <el-select v-model="timeRange" size="small" class="time-select">
              <el-option label="今日" value="today"></el-option>
              <el-option label="本周" value="week"></el-option>
              <el-option label="本月" value="month"></el-option>
              <el-option label="全年" value="year"></el-option>
            </el-select>
          </div>
        </template>
        <div class="chart-content">
          <div ref="taskTrendChart" class="chart"></div>
        </div>
      </el-card>

      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>任务分类占比</span>
          </div>
        </template>
        <div class="chart-content">
          <div ref="taskCategoryChart" class="chart"></div>
        </div>
      </el-card>
    </div>

    <div class="recent-tasks-container">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>最近任务</span>
            <el-button type="text" size="small" @click="navigateToTasks">查看全部</el-button>
          </div>
        </template>
        <el-table :data="recentTasks" stripe class="tasks-table">
          <el-table-column prop="id" label="任务ID" width="80"></el-table-column>
          <el-table-column prop="name" label="任务名称" width="200"></el-table-column>
          <el-table-column prop="category" label="分类" width="100"></el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'completed' ? 'success' : 'warning'">{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="deadline" label="截止日期" width="150"></el-table-column>
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="viewTaskDetail(scope.row.id)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { List, Check, Clock, Cpu, BarChart, PieChart as PieChartIcon }
  from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 响应式数据
const totalTasks = ref(128)
const completedTasks = ref(96)
const pendingTasks = ref(32)
const aiCalls = ref(245)
const timeRange = ref('month')
const recentTasks = ref([
  { id: 1001, name: '数据备份与同步', category: '系统', status: 'completed', deadline: '2023-11-15' },
  { id: 1002, name: '用户行为分析报告', category: '分析', status: 'completed', deadline: '2023-11-18' },
  { id: 1003, name: '服务器性能优化', category: '维护', status: 'pending', deadline: '2023-11-25' },
  { id: 1004, name: '新功能需求调研', category: '产品', status: 'pending', deadline: '2023-11-30' },
  { id: 1005, name: '安全漏洞扫描', category: '安全', status: 'completed', deadline: '2023-11-10' }
])
const taskTrendChart = ref(null)
const taskCategoryChart = ref(null)
const router = useRouter()

// 生命周期钩子
onMounted(() => {
  initTaskTrendChart()
  initTaskCategoryChart()
})

// 初始化任务趋势图表
const initTaskTrendChart = () => {
  const chartDom = taskTrendChart.value
  if (chartDom) {
    const myChart = echarts.init(chartDom)

    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['已完成', '待处理']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
          axisTick: {
            alignWithLabel: true
          }
        }
      ],
      yAxis: [
        {
          type: 'value'
        }
      ],
      series: [
        {
          name: '已完成',
          type: 'bar',
          barWidth: '60%',
          data: [65, 78, 85, 76, 88, 92, 86, 95, 90, 98, 105, 110]
        },
        {
          name: '待处理',
          type: 'bar',
          barWidth: '60%',
          data: [35, 30, 25, 32, 28, 22, 26, 20, 25, 18, 15, 12]
        }
      ]
    }

    myChart.setOption(option)

    // 窗口大小改变时重新调整图表大小
    window.addEventListener('resize', () => {
      myChart.resize()
    })
  }
}

// 初始化任务分类图表
const initTaskCategoryChart = () => {
  const chartDom = taskCategoryChart.value
  if (chartDom) {
    const myChart = echarts.init(chartDom)

    const option = {
      tooltip: {
        trigger: 'item'
      },
      legend: {
        top: '5%',
        left: 'center'
      },
      series: [
        {
          name: '任务分类',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: [
            {
              value: 40,
              name: '系统'
            },
            {
              value: 30,
              name: '分析'
            },
            {
              value: 20,
              name: '维护'
            },
            {
              value: 15,
              name: '产品'
            },
            {
              value: 10,
              name: '安全'
            }
          ]
        }
      ]
    }

    myChart.setOption(option)

    // 窗口大小改变时重新调整图表大小
    window.addEventListener('resize', () => {
      myChart.resize()
    })
  }
}

// 导航到任务列表
const navigateToTasks = () => {
  router.push('/tasks')
}

// 查看任务详情
const viewTaskDetail = (id) => {
  router.push(`/tasks/${id}`)
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #4096ff 0%, #73c0de 100%);
  color: #fff;
  overflow: hidden;
}

.welcome-content {
  padding: 40px 20px;
  text-align: center;
}

.welcome-content h1 {
  font-size: 24px;
  margin-bottom: 10px;
}

.welcome-content p {
  font-size: 16px;
  margin-bottom: 20px;
}

.stats-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  flex: 1;
  min-width: 200px;
  max-width: calc(25% - 20px);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.stat-change {
  font-size: 12px;
}

.increase {
  color: #198754;
}

.decrease {
  color: #dc3545;
}

.stat-icon {
  font-size: 28px;
  color: #4096ff;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.charts-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  flex: 1;
  min-width: 300px;
  max-width: calc(50% - 20px);
  height: 300px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.time-select {
  width: 100px;
}

.chart-content {
  height: calc(100% - 50px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart {
  width: 100%;
  height: 100%;
}

.recent-tasks-container {
  margin-top: 20px;
}

.tasks-table {
  width: 100%;
}</style>