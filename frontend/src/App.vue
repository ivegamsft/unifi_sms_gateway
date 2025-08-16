<template>
  <div id="app">
    <div v-if="!isLoggedIn" class="login-container">
      <LoginForm @login-success="handleLoginSuccess" />
    </div>
    <div v-else class="dashboard-container">
      <Dashboard :user="currentUser" @logout="handleLogout" />
    </div>
  </div>
</template>

<script>
import LoginForm from './components/LoginForm.vue'
import Dashboard from './components/Dashboard.vue'

export default {
  name: 'App',
  components: {
    LoginForm,
    Dashboard
  },
  data() {
    return {
      isLoggedIn: false,
      currentUser: null
    }
  },
  mounted() {
    // Check if user is already logged in
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('user')
    if (token && user) {
      this.isLoggedIn = true
      this.currentUser = JSON.parse(user)
    }
  },
  methods: {
    handleLoginSuccess(userData) {
      this.isLoggedIn = true
      this.currentUser = userData.user
      localStorage.setItem('token', userData.token)
      localStorage.setItem('user', JSON.stringify(userData.user))
    },
    handleLogout() {
      this.isLoggedIn = false
      this.currentUser = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
}
</script>

<style>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.dashboard-container {
  min-height: 100vh;
  padding: 20px;
}
</style>
