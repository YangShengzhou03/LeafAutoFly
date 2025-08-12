<template>
  <div class="home">
    <h1>{{ $t('welcome') }}</h1>
    <p>{{ $t('home.description') }}</p>
    
    <div class="action-buttons">
      <BaseButton 
        v-if="isAuthenticated" 
        @click="$router.push('/examples')"
        class="primary"
      >
        {{ $t('home.viewExamples') }}
      </BaseButton>
      
      <div v-else class="auth-buttons">
        <BaseButton @click="$router.push('/login')" class="primary">
          {{ $t('auth.login') }}
        </BaseButton>
        <BaseButton @click="$router.push('/register')" class="secondary">
          {{ $t('auth.register') }}
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Home',
  computed: {
    ...mapGetters(['isAuthenticated'])
  }
}
</script>

<style scoped>
.home {
  text-align: center;
  padding: 40px 20px;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

p {
  font-size: 1.2rem;
  max-width: 800px;
  margin: 0 auto 30px;
  line-height: 1.6;
}

.action-buttons {
  margin-top: 30px;
}

.auth-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}
</style>
