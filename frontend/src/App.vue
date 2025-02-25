<template>
  <div
    id="app"
    class="bg-gray-100 min-h-screen"
  >
    <header class="bg-blue-500 text-white text-center py-4">
      <h1 class="text-xl font-bold">
        MedConnect
      </h1>
    </header>
    
    <main class="pt-6">
      <!-- Router outlet -->
      <router-view />
    </main>
    
    <footer class="bg-gray-800 text-white text-center py-2">
      <p class="text-sm">
        &copy; 2025 MedConnect. All rights reserved.
      </p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Global styles */
body {
  margin: 0;
  font-family: "Arial", sans-serif;
}
</style>
