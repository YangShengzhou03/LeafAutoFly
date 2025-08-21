<template>
  <div class="app-container">
    <div class="main-content">
      <div class="top-row">
        <div class="otherbox-section">
          <el-card class="otherbox-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <div class="header-title">
                  <span>数据导出中心</span>
                </div>
              </div>
            </template>

            <div class="function-grid">
              <!-- 导出功能卡片 -->
              <div class="function-card" @click="exportGroupMembers">
                <div class="card-icon">
                  <i class="el-icon-user-solid"></i>
                </div>
                <div class="card-title">群成员导出</div>
              </div>

              <div class="function-card" @click="exportGroupMessages">
                <div class="card-icon">
                  <i class="el-icon-chat-line-round"></i>
                </div>
                <div class="card-title">消息记录导出</div>
              </div>

              <div class="function-card" @click="exportGroupFiles">
                <div class="card-icon">
                  <i class="el-icon-folder"></i>
                </div>
                <div class="card-title">文件数据导出</div>
              </div>

              <div class="function-card" @click="exportGroupImages">
                <div class="card-icon">
                  <i class="el-icon-picture"></i>
                </div>
                <div class="card-title">图片数据导出</div>
              </div>

              <div class="function-card" @click="exportGroupVoices">
                <div class="card-icon">
                  <i class="el-icon-mic"></i>
                </div>
                <div class="card-title">语音数据导出</div>
              </div>

              <div class="function-card" @click="exportGroupVideos">
                <div class="card-icon">
                  <i class="el-icon-video-camera"></i>
                </div>
                <div class="card-title">视频数据导出</div>
              </div>

              <div class="function-card" @click="exportGroupLinks">
                <div class="card-icon">
                  <i class="el-icon-link"></i>
                </div>
                <div class="card-title">链接数据导出</div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  padding: 20px;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}

.top-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.otherbox-card {
  border-radius: 8px;
}

.function-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
  padding: 16px;
}

.function-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
}

.function-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.function-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-color: #93c5fd;
}

.function-card:hover::before {
  transform: scaleX(1);
}

.function-card:active {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.card-icon {
  font-size: 32px;
  color: #3b82f6;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.function-card:hover .card-icon {
  color: #1d4ed8;
  transform: scale(1.1);
}

.card-title {
  font-size: 15px;
  color: #1e293b;
  text-align: center;
  font-weight: 500;
  transition: color 0.3s ease;
}

.function-card:hover .card-title {
  color: #1d4ed8;
}

@media (max-width: 768px) {
  .function-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>

<script>
export default {
  methods: {
    exportGroupMembers() {
      console.log('群成员导出');
    },
    exportGroupMessages() {
      console.log('消息记录导出');
    },
    exportGroupFiles() {
      console.log('文件数据导出');
    },
    exportGroupImages() {
      console.log('图片数据导出');
    },
    exportGroupVoices() {
      console.log('语音数据导出');
    },
    exportGroupVideos() {
      console.log('视频数据导出');
    },
    exportGroupLinks() {
      console.log('链接数据导出');
    }
  }
}
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


.main-content {
  padding: 0;
  max-width: 100vw;
  margin: 0 auto;
}


.top-row {
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


.el-row {
  margin-bottom: 20px;
}


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


.el-table .el-button {
  margin: 0 4px;
  padding: 4px 8px;
  font-size: 12px;
}


.custom-input .el-input__wrapper {
  border-radius: 8px;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.custom-input .el-input__wrapper:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}


.custom-select .el-input__wrapper {
  border-radius: 8px;
  border: 1px solid var(--border-color);
}



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

.el-table--enable-row-hover .el-table__body tr:hover>td {
  background-color: var(--light-color);
}


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


.custom-pagination {
  padding: 16px 0;
  display: flex;
  justify-content: flex-end;
}


.custom-rules-container {
  border: 0;
  border-radius: 12px;
  padding: 0;
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
