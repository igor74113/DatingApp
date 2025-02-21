<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input
        v-model="username"
        placeholder="Username"
        required
      >
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      >
      <button type="submit">
        Login
      </button>
    </form>
    <p
      v-if="error"
      class="text-red-500"
    >
      {{ error }}
    </p>
  </div>
</template>

<script>
import api from '../api/api';

export default {
  data() {
    return { username: "", password: "", error: "" };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await api.post('token/', {
          username: this.username,
          password: this.password,
        });

        localStorage.setItem('token', response.data.access);  // Store JWT token
        this.$router.push('/profile-setup');  // Redirect to profile page
      } catch (error) {
        this.error = "Invalid credentials";
      }
    }
  }
};
</script>
