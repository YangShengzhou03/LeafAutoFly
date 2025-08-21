<template>
  <div class="otherbox-container">
    <div class="otherbox-card">
      <div class="otherbox-header">
        <div class="header-title">
          <span>百宝箱</span>
        </div>
      </div>

      <div class="function-grid">
        <!-- 导出功能卡片 -->
        <div class="function-card" @click="exportGroupMembers">
          <div class="card-icon">
            <i class="el-icon-user-solid"></i>
          </div>
          <div class="card-title">导出群聊成员数据</div>
        </div>

        <div class="function-card" @click="exportGroupMessages">
          <div class="card-icon">
            <i class="el-icon-chat-line-round"></i>
          </div>
          <div class="card-title">导出群聊消息数据</div>
        </div>

        <div class="function-card" @click="exportGroupFiles">
          <div class="card-icon">
            <i class="el-icon-folder"></i>
          </div>
          <div class="card-title">导出群聊文件数据</div>
        </div>

        <div class="function-card" @click="exportGroupImages">
          <div class="card-icon">
            <i class="el-icon-picture"></i>
          </div>
          <div class="card-title">导出群聊图片数据</div>
        </div>

        <div class="function-card" @click="exportGroupVoices">
          <div class="card-icon">
            <i class="el-icon-mic"></i>
          </div>
          <div class="card-title">导出群聊语音数据</div>
        </div>

        <div class="function-card" @click="exportGroupVideos">
          <div class="card-icon">
            <i class="el-icon-video-camera"></i>
          </div>
          <div class="card-title">导出群聊视频数据</div>
        </div>

        <div class="function-card" @click="exportGroupLinks">
          <div class="card-icon">
            <i class="el-icon-link"></i>
          </div>
          <div class="card-title">导出群聊链接数据</div>
        </div>

        <!-- 重复功能卡片（根据需求保留或修改） -->
        <div class="function-card" @click="exportGroupFiles2">
          <div class="card-icon">
            <i class="el-icon-folder-opened"></i>
          </div>
          <div class="card-title">导出群聊文件数据2</div>
        </div>

        <div class="function-card" @click="exportGroupImages2">
          <div class="card-icon">
            <i class="el-icon-picture-outline"></i>
          </div>
          <div class="card-title">导出群聊图片数据2</div>
        </div>

        <div class="function-card" @click="exportGroupVoices2">
          <div class="card-icon">
            <i class="el-icon-headset"></i>
          </div>
          <div class="card-title">导出群聊语音数据2</div>
        </div>

        <div class="function-card" @click="exportGroupVideos2">
          <div class="card-icon">
            <i class="el-icon-video-pause"></i>
          </div>
          <div class="card-title">导出群聊视频数据2</div>
        </div>

        <div class="function-card" @click="exportGroupLinks2">
          <div class="card-icon">
            <i class="el-icon-connection"></i>
          </div>
          <div class="card-title">导出群聊链接数据2</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    exportGroupMembers() {
      // 跳转到导出群聊成员数据页面
      console.log('导出群聊成员数据');
    },
    exportGroupMessages() {
      console.log('导出群聊消息数据');
    },
    exportGroupFiles() {
      console.log('导出群聊文件数据');
    },
    exportGroupImages() {
      console.log('导出群聊图片数据');
    },
    exportGroupVoices() {
      console.log('导出群聊语音数据');
    },
    exportGroupVideos() {
      console.log('导出群聊视频数据');
    },
    exportGroupLinks() {
      console.log('导出群聊链接数据');
    },
    exportGroupFiles2() {
      console.log('导出群聊文件数据2');
    },
    exportGroupImages2() {
      console.log('导出群聊图片数据2');
    },
    exportGroupVoices2() {
      console.log('导出群聊语音数据2');
    },
    exportGroupVideos2() {
      console.log('导出群聊视频数据2');
    },
    exportGroupLinks2() {
      console.log('导出群聊链接数据2');
    }
  }
}
</script>

<style scoped>
.otherbox-container {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.otherbox-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.otherbox-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.function-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.function-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #eee;
}

.function-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  background-color: #f0f7ff;
  border-color: #d0e3ff;
}

.card-icon {
  font-size: 32px;
  color: #409EFF;
  margin-bottom: 10px;
}

.card-title {
  font-size: 14px;
  color: #666;
  text-align: center;
  word-break: break-word;
}
</style>
