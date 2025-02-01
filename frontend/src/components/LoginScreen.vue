<template>
  <div class="h-screen flex flex-col items-center justify-center bg-gray-50">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Login</h2>
    <form @submit.prevent="handleLogin" class="w-80 space-y-4">
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full px-4 py-2 border rounded-lg"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="w-full px-4 py-2 border rounded-lg"
      />
      <button type="submit" class="w-full py-2 bg-blue-500 text-white rounded-lg">
        Login
      </button>
    </form>

    <router-link to="/profile-setup" class="text-sm text-blue-500 mt-2">
      Forgot Password?
    </router-link>
  </div>
</template>

<script>
export default {
  name: "LoginScreen",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    handleLogin() {
      console.log("Logging in with:", this.email, this.password);
      // Handle login logic or call an API
    },
  },
};
</script>
