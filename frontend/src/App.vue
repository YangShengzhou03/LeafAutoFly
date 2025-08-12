<template>
  <div id="app">
    <Navbar v-if="isAuthenticated" />
    <main class="container">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script>
import Navbar from './components/layout/Navbar.vue'
import Footer from './components/layout/Footer.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer
  },
  computed: {
    ...mapGetters(['isAuthenticated'])
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  padding: 20px 0;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}
</style>
