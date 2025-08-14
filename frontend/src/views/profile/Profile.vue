<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>个人资料</span>
        </div>
      </template>

      <div class="profile-content">
        <div class="profile-avatar-container">
          <img
            :src="userInfo.avatar"
            alt="用户头像"
            class="profile-avatar"
          />
          <el-button type="primary" size="small" @click="uploadAvatar"
            >更换头像</el-button
          >
        </div>

        <el-form
          ref="profileFormRef"
          :model="userInfo"
          :rules="profileRules"
          label-width="100px"
          class="profile-form"
        >
          <el-form-item prop="username">
            <el-input v-model="userInfo.username" placeholder="用户名"></el-input>
          </el-form-item>

          <el-form-item prop="email">
            <el-input v-model="userInfo.email" placeholder="邮箱"></el-input>
          </el-form-item>

          <el-form-item prop="phone">
            <el-input v-model="userInfo.phone" placeholder="手机号"></el-input>
          </el-form-item>

          <el-form-item prop="department">
            <el-input v-model="userInfo.department" placeholder="部门"></el-input>
          </el-form-item>

          <el-form-item prop="position">
            <el-input v-model="userInfo.position" placeholder="职位"></el-input>
          </el-form-item>

          <el-form-item prop="introduction">
            <el-input
              v-model="userInfo.introduction"
              type="textarea"
              placeholder="个人简介"
              rows="4"
            ></el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleSave">保存修改</el-button>
            <el-button @click="handleCancel" style="margin-left: 10px;">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <el-card class="security-card">
      <template #header>
        <div class="card-header">
          <span>安全设置</span>
        </div>
      </template>

      <div class="security-content">
        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-width="100px"
          class="password-form"
        >
          <el-form-item prop="oldPassword">
            <el-input
              v-model="passwordForm.oldPassword"
              type="password"
              placeholder="旧密码"
            ></el-input>
          </el-form-item>

          <el-form-item prop="newPassword">
            <el-input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="新密码"
            ></el-input>
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="passwordForm.confirmPassword"
              type="password"
              placeholder="确认新密码"
            ></el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleChangePassword">修改密码</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElUpload } from 'element-plus'
import { User, Lock, Mail, Phone, Building, Briefcase, InfoFilled, Upload }
  from '@element-plus/icons-vue'

// 响应式数据
const userInfo = ref({
  username: '',
  email: '',
  phone: '',
  department: '',
  position: '',
  introduction: '',
  avatar: 'https://via.placeholder.com/100?text=User'
})

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const profileFormRef = ref(null)
const passwordFormRef = ref(null)
const router = useRouter()
const profileRules = {
  username: [
    {
      required: true,
      message: '请输入用户名',
      trigger: 'blur'
    }
  ],
  email: [
    {
      required: true,
      message: '请输入邮箱',
      trigger: 'blur'
    },
    {
      type: 'email',
      message: '请输入有效的邮箱地址',
      trigger: 'blur'
    }
  ],
  phone: [
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入有效的手机号码',
      trigger: 'blur'
    }
  ]
}

const passwordRules = {
  oldPassword: [
    {
      required: true,
      message: '请输入旧密码',
      trigger: 'blur'
    }
  ],
  newPassword: [
    {
      required: true,
      message: '请输入新密码',
      trigger: 'blur'
    },
    {
      min: 6,
      max: 20,
      message: '密码长度在 6 到 20 个字符之间',
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    {
      required: true,
      message: '请确认新密码',
      trigger: 'blur'
    },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 生命周期钩子
onMounted(() => {
  fetchUserInfo()
})

// 模拟获取用户信息
const fetchUserInfo = () => {
  // 模拟API请求
  setTimeout(() => {
    userInfo.value = {
      username: '张三',
      email: 'zhangsan@example.com',
      phone: '13800138000',
      department: '技术部',
      position: '前端开发工程师',
      introduction: '我是一名有5年经验的前端开发工程师，擅长Vue、React等前端框架。',
      avatar: 'https://via.placeholder.com/100?text=User'
    }
  }, 500)
}

// 上传头像
const uploadAvatar = () => {
  ElMessage.info('头像上传功能待实现')
  // 实际应用中，这里应该使用el-upload组件实现文件上传
}

// 保存个人资料
const handleSave = () => {
  profileFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟保存操作
      setTimeout(() => {
        ElMessage.success('个人资料保存成功')
      }, 500)
    }
  })
}

// 取消修改
const handleCancel = () => {
  fetchUserInfo() // 重置表单
}

// 修改密码
const handleChangePassword = () => {
  passwordFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟修改密码操作
      setTimeout(() => {
        ElMessage.success('密码修改成功，请重新登录')
        // 重置密码表单
        passwordForm.value = {
          oldPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
        // 这里可以添加登出逻辑
      }, 500)
    }
  })
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-card,
.security-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-content {
  padding: 20px;
}

.profile-avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin-bottom: 15px;
  object-fit: cover;
}

.profile-form,
.password-form {
  max-width: 600px;
  margin: 0 auto;
}

.security-content {
  padding: 20px;
}
</style>