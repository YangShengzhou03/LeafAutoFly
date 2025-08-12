<template>
  <div class="ai-service-container">
    <el-card class="service-card">
      <template #header>
        <div class="card-header">
          <span>AI 服务</span>
        </div>
      </template>

      <div class="service-intro">
        <p>欢迎使用 LeafAuto 智能管理系统的 AI 服务。这里提供多种 AI 辅助功能，帮助您更高效地完成工作。</p>
      </div>

      <div class="service-tabs">
        <el-tabs v-model="activeTab" type="border-card">
          <el-tab-pane label="文本生成">
            <div class="tab-content">
              <el-form :model="textGenerationForm">
                <el-form-item label="生成类型">
                  <el-select v-model="textGenerationForm.type" placeholder="请选择生成类型">
                    <el-option label="邮件" value="email"></el-option>
                    <el-option label="报告" value="report"></el-option>
                    <el-option label="总结" value="summary"></el-option>
                    <el-option label="其他" value="other"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="输入内容">
                  <el-input
                    v-model="textGenerationForm.input"
                    type="textarea"
                    placeholder="请输入需要处理的文本..."
                    rows="4"
                  ></el-input>
                </el-form-item>
                <el-form-item label="生成长度">
                  <el-slider
                    v-model="textGenerationForm.length"
                    :min="100"
                    :max="2000"
                    :step="100"
                    show-input
                  ></el-slider>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="generateText">生成文本</el-button>
                </el-form-item>
              </el-form>

              <div v-if="textGenerationResult" class="result-container">
                <h3>生成结果</h3>
                <el-input
                  v-model="textGenerationResult"
                  type="textarea"
                  rows="6"
                  readonly
                ></el-input>
                <el-button type="primary" size="small" @click="copyTextResult" style="margin-top: 10px;">复制结果</el-button>
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="图像处理">
            <div class="tab-content">
              <el-form :model="imageProcessingForm">
                <el-form-item label="处理类型">
                  <el-select v-model="imageProcessingForm.type" placeholder="请选择处理类型">
                    <el-option label="图像增强" value="enhance"></el-option>
                    <el-option label="风格转换" value="style_transfer"></el-option>
                    <el-option label="目标检测" value="object_detection"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="上传图片">
                  <el-upload
                    class="upload-demo"
                    action="#"
                    :on-change="handleImageUpload"
                    :auto-upload="false"
                    :show-file-list="true"
                  >
                    <el-button type="primary">点击上传</el-button>
                  </el-upload>
                </el-form-item>
                <el-form-item v-if="imageProcessingForm.type === 'style_transfer'" label="风格选择">
                  <el-select v-model="imageProcessingForm.style" placeholder="请选择风格">
                    <el-option label="油画" value="oil_painting"></el-option>
                    <el-option label="水彩" value="watercolor"></el-option>
                    <el-option label="素描" value="sketch"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="processImage" :disabled="!imageProcessingForm.file">处理图片</el-button>
                </el-form-item>
              </el-form>

              <div v-if="imageProcessingResult" class="result-container">
                <h3>处理结果</h3>
                <div class="image-result">
                  <img :src="imageProcessingResult" alt="处理结果">
                </div>
                <el-button type="primary" size="small" @click="downloadImageResult" style="margin-top: 10px;">下载图片</el-button>
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="数据分析">
            <div class="tab-content">
              <el-form :model="dataAnalysisForm">
                <el-form-item label="分析类型">
                  <el-select v-model="dataAnalysisForm.type" placeholder="请选择分析类型">
                    <el-option label="趋势分析" value="trend"></el-option>
                    <el-option label="聚类分析" value="cluster"></el-option>
                    <el-option label="关联分析" value="association"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="上传数据">
                  <el-upload
                    class="upload-demo"
                    action="#"
                    :on-change="handleDataUpload"
                    :auto-upload="false"
                    :show-file-list="true"
                    accept=".csv,.xlsx,.xls"
                  >
                    <el-button type="primary">点击上传</el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        支持 CSV、Excel 格式文件
                      </div>
                    </template>
                  </el-upload>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="analyzeData" :disabled="!dataAnalysisForm.file">分析数据</el-button>
                </el-form-item>
              </el-form>

              <div v-if="dataAnalysisResult" class="result-container">
                <h3>分析结果</h3>
                <div ref="dataAnalysisChart" class="chart"></div>
                <el-button type="primary" size="small" @click="downloadDataReport" style="margin-top: 10px;">下载报告</el-button>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  FileText,
  Image as ImageIcon,
  BarChart2,
  Download,
  Copy,
  Send
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 响应式数据
const activeTab = ref('0')
const textGenerationForm = ref({
  type: 'email',
  input: '',
  length: 500
})
const textGenerationResult = ref('')
const imageProcessingForm = ref({
  type: 'enhance',
  file: null,
  style: 'oil_painting'
})
const imageProcessingResult = ref('')
const dataAnalysisForm = ref({
  type: 'trend',
  file: null
})
const dataAnalysisResult = ref(null)
const dataAnalysisChart = ref(null)
const chartInstance = ref(null)

// 生命周期钩子
onMounted(() => {
  // 初始化图表实例
  nextTick(() => {
    if (dataAnalysisChart.value) {
      chartInstance.value = echarts.init(dataAnalysisChart.value)
    }
  })
})

// 监听dataAnalysisChart变化
watch(dataAnalysisChart, (newValue) => {
  if (newValue && !chartInstance.value) {
    chartInstance.value = echarts.init(newValue)
  }
})

// 生成文本
const generateText = () => {
  if (!textGenerationForm.value.input.trim()) {
    ElMessage.warning('请输入需要处理的文本')
    return
  }

  // 模拟AI生成
  ElMessage.info('正在生成文本...')
  setTimeout(() => {
    // 模拟生成结果
    let result = ''
    if (textGenerationForm.value.type === 'email') {
      result = `主题: 关于${textGenerationForm.value.input.substring(0, 20)}...\n\n尊敬的客户,\n\n${textGenerationForm.value.input}\n\n此致\n敬礼\nLeafAuto 团队`
    } else if (textGenerationForm.value.type === 'report') {
      result = `# 报告: ${textGenerationForm.value.input.substring(0, 20)}...\n\n## 概述\n${textGenerationForm.value.input}\n\n## 分析\n根据提供的信息，我们进行了详细分析...\n\n## 结论\n基于以上分析，我们建议...`
    } else if (textGenerationForm.value.type === 'summary') {
      result = `### 总结\n${textGenerationForm.value.input.substring(0, Math.min(textGenerationForm.value.input.length, textGenerationForm.value.length))}...`
    } else {
      result = textGenerationForm.value.input
    }

    textGenerationResult.value = result
    ElMessage.success('文本生成成功')
  }, 1500)
}

// 复制文本结果
const copyTextResult = () => {
  navigator.clipboard.writeText(textGenerationResult.value)
    .then(() => {
      ElMessage.success('复制成功')
    })
    .catch(() => {
      ElMessage.error('复制失败，请手动复制')
    })
}

// 处理图片上传
const handleImageUpload = (file) => {
  imageProcessingForm.value.file = file.raw
}

// 处理图片
const processImage = () => {
  // 模拟AI处理
  ElMessage.info('正在处理图片...')
  setTimeout(() => {
    // 模拟处理结果，这里使用一个占位图URL
    imageProcessingResult.value = 'https://via.placeholder.com/500x300?text=Processed+Image'
    ElMessage.success('图片处理成功')
  }, 2000)
}

// 下载图片结果
const downloadImageResult = () => {
  // 模拟下载
  const link = document.createElement('a')
  link.href = imageProcessingResult.value
  link.download = 'processed-image.png'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  ElMessage.success('图片下载成功')
}

// 处理数据上传
const handleDataUpload = (file) => {
  dataAnalysisForm.value.file = file.raw
}

// 分析数据
const analyzeData = () => {
  // 模拟AI分析
  ElMessage.info('正在分析数据...')
  setTimeout(() => {
    dataAnalysisResult.value = true
    // 模拟生成图表
    if (chartInstance.value) {
      const option = {
        title: {
          text: '数据分析结果',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['数据1', '数据2'],
          bottom: 0
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['1月', '2月', '3月', '4月', '5月', '6月']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '数据1',
            type: 'line',
            stack: 'Total',
            data: [120, 132, 101, 134, 90, 230]
          },
          {
            name: '数据2',
            type: 'line',
            stack: 'Total',
            data: [220, 182, 191, 234, 290, 330]
          }
        ]
      }
      chartInstance.value.setOption(option)
    }
    ElMessage.success('数据分析成功')
  }, 2000)
}

// 下载数据报告
const downloadDataReport = () => {
  // 模拟下载
  ElMessage.success('报告下载成功')
}
</script>

<style scoped>
.ai-service-container {
  padding: 20px;
}

.service-card {
  margin-bottom: 20px;
}

.service-intro {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 5px;
}

.service-tabs {
  margin-top: 20px;
}

.tab-content {
  padding: 20px;
}

.result-container {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 5px;
}

.image-result {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.image-result img {
  max-width: 100%;
  max-height: 400px;
  border-radius: 5px;
}

.chart {
  width: 100%;
  height: 400px;
  margin-top: 10px;
}
</style>