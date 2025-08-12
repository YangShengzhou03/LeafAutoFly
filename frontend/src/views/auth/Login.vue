<template>
  <div class="login-container">
    <BaseCard title="登录">
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">{{ $t('auth.username') }}</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            :placeholder="$t('auth.enterUsername')"
          >
        </div>
        
        <div class="form-group">
          <label for="password">{{ $t('auth.password') }}</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            :placeholder="$t('auth.enterPassword')"
          >
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div class="form-actions">
          <BaseButton type="submit" :loading="loading" class="primary full-width">
            {{ $t('auth.login') }}
          </BaseButton>
        </div>
      </form>
      
      <div class="register-link">
        {{ $t('auth.noAccount') }}
        <a @click="$router.push('/register')">{{ $t('auth.registerNow') }}</a>
      </div>
    </BaseCard>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  computed: {
    ...mapState('auth', ['loading', 'error'])
  },
  methods: {
    ...mapActions('auth', ['login']),
    async handleLogin() {
      try {
        await this.login({ username: this.username, password: this.password })
        this.$router.push('/examples')
        this.$message.success(this.$t('auth.loginSuccess'))
      } catch (err) {
        // 错误信息会通过mapState获取
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 40px auto;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.error-message {
  color: #dc3545;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 4px;
}

.form-actions {
  margin-top: 30px;
}

.register-link {
  margin-top: 20px;
  text-align: center;
}

.register-link a {
  color: #007bff;
  cursor: pointer;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

.full-width {
  width: 100%;
}
</style>
