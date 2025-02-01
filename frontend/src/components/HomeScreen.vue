<!-- HomeScreen.vue -->
<template>
  <div class="h-screen flex flex-col items-center justify-center bg-white">
    <img src="@/assets/logo.png" alt="App Logo" class="w-24 mb-6" />
    <h1 class="text-3xl font-bold text-gray-800 mb-12">Welcome to MedConnect</h1>
    <div class="space-y-4">
      <router-link
        to="/login"
        class="w-64 py-2 bg-blue-500 text-white rounded-lg shadow text-center block"
      >
        Login
      </router-link>
      <router-link
        to="/profile-setup"
        class="w-64 py-2 bg-gray-200 text-gray-800 rounded-lg shadow text-center block"
      >
        Sign Up
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeScreen",
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
