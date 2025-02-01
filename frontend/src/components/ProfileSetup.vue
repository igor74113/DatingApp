<template>
  <div class="h-screen flex flex-col items-center justify-center bg-gray-50">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Set Up Your Profile</h2>
    <form class="w-80 space-y-4">
      <input type="text" placeholder="Full Name" class="w-full px-4 py-2 border rounded-lg" />
      <input type="text" placeholder="Job Title" class="w-full px-4 py-2 border rounded-lg" />
      <textarea
        placeholder="Short Bio"
        class="w-full px-4 py-2 border rounded-lg"
      ></textarea>
      <button type="submit" class="w-full py-2 bg-green-500 text-white rounded-lg">
        Save Profile
      </button>
    </form>
  </div>
</template>

<script>
export default {
  name: "ProfileSetup",
};
</script>
