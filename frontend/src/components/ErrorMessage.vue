<script setup>
defineProps({
  message: { type: String, required: true },
})
</script>

<template>
  <div
    role="alert"
    class="flex items-center gap-3 rounded-xl bg-red-500/90 px-4 py-3 text-white shadow-lg"
  >
    <span class="text-xl">⚠️</span>
    <p>{{ message }}</p>
  </div>
</template>
