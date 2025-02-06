<template>
  <div class="h-screen bg-gray-100">
    <h1 class="text-xl font-bold text-center">
      Discover Matches
    </h1>
    <div
      v-for="match in matches"
      :key="match.id"
      class="match-card"
    >
      <h3>{{ match.user2.username }}</h3>
      <p>Score: {{ match.match_score }}</p>
    </div>
  </div>
</template>

<script>
import api from '@/api/api'; 

export default {
  data() {
    return { matches: [] };
  },
  mounted() {
    this.fetchMatches();
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
  }
};
</script>

<style>
.match-card { background: white; padding: 10px; margin: 10px; border-radius: 5px; }
</style>
