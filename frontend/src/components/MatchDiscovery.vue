<template>
  <div class="h-screen bg-gray-100">
    <div class="h-16 bg-white shadow flex items-center px-4">
      <h1 class="text-xl font-bold">Discover Matches</h1>
    </div>
    <div class="flex flex-col items-center mt-6 space-y-4">
      <!-- Profile card -->
      <div class="w-72 h-96 bg-white shadow rounded-lg flex flex-col items-center justify-center">
        <img src="/profile.jpg" alt="User Profile" class="w-32 h-32 rounded-full mb-4" />
        <h3 class="text-lg font-semibold">Dr. Jane Doe</h3>
        <p class="text-sm text-gray-500">Cardiologist, NY</p>
      </div>

      <!-- Like & Settings buttons -->
      <div class="flex space-x-6">
        <router-link
          to="/chat"
          class="w-16 h-16 bg-blue-500 text-white rounded-full shadow text-center flex items-center justify-center"
        >
          &#10084;
        </router-link>
        <router-link
          to="/settings"
          class="w-16 h-16 bg-gray-300 rounded-full shadow text-center flex items-center justify-center"
        >
          &#9881;
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MatchDiscovery",
};
</script>
