<template>
  <div class="register-container">
    <div class="register-box">
      <div class="logo-container">
        <img src="@/assets/images/logo.png" alt="Logo" class="logo" />
        <h2 class="title">LeafAuto 智能管理系统</h2>
      </div>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            :validate-event="false"
          ></el-input>
        </el-form-item>
        <el-form-item prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱"
            prefix-icon="Message"
            :validate-event="false"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            :show-password="showPassword"
            :validate-event="false"
          ></el-input>
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请确认密码"
            prefix-icon="Lock"
            :show-password="showConfirmPassword"
            :validate-event="false"
          ></el-input>
        </el-form-item>
        <el-form-item prop="verifyCode">
          <div class="verify-code-container">
            <el-input
              v-model="registerForm.verifyCode"
              placeholder="请输入验证码"
              prefix-icon="Key"
              :validate-event="false"
              style="width: 65%"
            ></el-input>
            <el-button
              type="primary"
              :disabled="countdown > 0"
              style="width: 30%"
              @click="sendVerifyCode"
            >
              {{ countdown > 0 ? `${countdown}s 后重新发送` : '发送验证码' }}
            </el-button>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            style="width: 100%"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
        <el-form-item>
          <div class="login-link">
            已有账号? <el-button type="text" @click="handleLogin">立即登录</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Key, Eye, EyeOff }
  from '@element-plus/icons-vue'

// 响应式数据
const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  verifyCode: ''
})
const registerFormRef = ref(null)
const loading = ref(false)
const countdown = ref(0)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const router = useRouter()
let timer = null

// 表单验证规则
const registerRules = {
  username: [
    {
      required: true,
      message: '请输入用户名',
      trigger: 'blur'
    },
    {
      min: 3,
      max: 20,
      message: '用户名长度在 3 到 20 个字符',
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
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: 'blur'
    },
    {
      min: 6,
      max: 20,
      message: '密码长度在 6 到 20 个字符',
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    {
      required: true,
      message: '请确认密码',
      trigger: 'blur'
    },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  verifyCode: [
    {
      required: true,
      message: '请输入验证码',
      trigger: 'blur'
    },
    {
      len: 6,
      message: '验证码长度为 6 个字符',
      trigger: 'blur'
    }
  ]
}

// 发送验证码
const sendVerifyCode = () => {
  registerFormRef.value.validateField('email', (error) => {
    if (!error) {
      // 模拟发送验证码
      countdown.value = 60
      ElMessage.success('验证码发送成功')

      timer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) {
          clearInterval(timer)
        }
      }, 1000)
    }
  })
}

// 处理注册
const handleRegister = () => {
  registerFormRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      // 模拟注册请求
      setTimeout(() => {
        // 这里可以替换为实际的注册API调用
        ElMessage.success('注册成功，请登录')
        router.push('/login')
        loading.value = false
      }, 1500)
    }
  })
}

// 处理登录
const handleLogin = () => {
  router.push('/login')
}

// 清理定时器
onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.register-box {
  width: 400px;
  padding: 30px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.logo {
  width: 60px;
  height: 60px;
  margin-bottom: 15px;
}

.title {
  font-size: 20px;
  color: #333;
  font-weight: bold;
}

.register-form {
  width: 100%;
}

.verify-code-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}
</style>