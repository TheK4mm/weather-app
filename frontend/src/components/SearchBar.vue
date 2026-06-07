<script setup>
import { ref } from 'vue'

defineProps({
  units: { type: String, default: 'metric' },
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['search', 'toggle-units'])

const query = ref('')

function submit() {
  emit('search', query.value)
}
</script>

<template>
  <div class="flex w-full max-w-xl flex-col gap-3 sm:flex-row">
    <div class="flex flex-1 overflow-hidden rounded-xl bg-white/95 shadow-lg">
      <input
        v-model="query"
        type="text"
        placeholder="Escribe una ciudad..."
        aria-label="Ciudad"
        class="flex-1 bg-transparent px-4 py-3 text-slate-800 outline-none placeholder:text-slate-400"
        @keyup.enter="submit"
      />
      <button
        class="bg-blue-600 px-5 font-medium text-white transition hover:bg-blue-700 disabled:opacity-60"
        :disabled="loading"
        @click="submit"
      >
        Buscar
      </button>
    </div>

    <button
      type="button"
      class="rounded-xl bg-white/20 px-4 py-3 font-medium text-white backdrop-blur transition hover:bg-white/30"
      :title="`Cambiar a ${units === 'metric' ? 'Fahrenheit' : 'Celsius'}`"
      @click="emit('toggle-units')"
    >
      {{ units === 'metric' ? '°C' : '°F' }}
    </button>
  </div>
</template>
