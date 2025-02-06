
<template>
  <div class="h-screen bg-gray-50">
    <div class="h-16 bg-white shadow flex items-center px-4">
      <h1 class="text-xl font-bold">
        Settings
      </h1>
    </div>
    <div class="p-4 space-y-4">
      <button class="w-full py-2 bg-gray-200 rounded-lg">
        Notification Preferences
      </button>
      <button class="w-full py-2 bg-gray-200 rounded-lg">
        Privacy Settings
      </button>
      <button class="w-full py-2 bg-gray-200 rounded-lg">
        Contact Support
      </button>
    </div>
  </div>
</template>

<script>
import api from '../api/api';  // Absolute pass for API import

export default {
  data() {
    return { matches: [] };
  },
  methods: {
    async fetchMatches() {
      try {
        const response = await api.get('matches/');
        this.matches = response.data;
      } catch (error) {
        console.error("Error fetching matches:", error);
      }
    }
  },
  mounted() {
    this.fetchMatches();
  }
};
</script>

