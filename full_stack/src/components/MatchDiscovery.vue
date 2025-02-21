<template>
  <div class="h-screen bg-gray-100 p-4">
    <h1 class="text-xl font-bold text-center mb-4">
      Discover Matches
    </h1>
    
    <div v-if="matches.length">
      <div v-for="match in matches" :key="match.id" class="match-card">
        <h3 class="text-lg font-semibold">{{ match.username }}</h3>
        <p class="text-gray-700">Score: <strong>{{ match.score }}</strong></p>
      </div>
    </div>
    
    <p v-else class="text-center text-gray-500">No matches found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { fetchMatches } from '@/api/api';

const matches = ref([]);

onMounted(async () => {
  try {
    matches.value = await fetchMatches();
  } catch (error) {
    console.error("Error fetching matches:", error);
  }
});
</script>


<style scoped>
.match-card {
  background: white;
  padding: 12px;
  margin: 10px;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
