<template>
  <div class="h-screen bg-gray-50">
    <div class="h-16 bg-white shadow flex items-center px-4">
      <h1 class="text-xl font-bold">Messages</h1>
    </div>
    <!-- Chat List -->
    <div class="space-y-4 p-4">
      <div class="flex items-center space-x-4 bg-white p-2 shadow rounded-lg">
        <img src="/avatar.jpg" alt="Avatar" class="w-12 h-12 rounded-full" />
        <div>
          <h3 class="text-sm font-semibold">Dr. John Smith</h3>
          <p class="text-xs text-gray-500">Let’s meet for coffee!</p>
        </div>
      </div>
      <!-- Add more conversation cards here -->
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatScreen",
};
</script>
