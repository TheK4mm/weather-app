<script setup>
import { computed } from 'vue'

const props = defineProps({
  day: { type: Object, required: true },
  units: { type: String, default: 'metric' },
})

// Día de la semana abreviado a partir de la fecha (mediodía local para evitar desfases).
const weekday = computed(() =>
  new Date(`${props.day.date}T12:00:00`).toLocaleDateString('es', { weekday: 'short' }),
)
</script>

<template>
  <div class="flex flex-col items-center gap-1 rounded-xl bg-white/90 p-3 text-slate-800 shadow">
    <span class="text-sm font-medium capitalize">{{ weekday }}</span>
    <img :src="day.icon" :alt="day.description" class="h-12 w-12" />
    <span class="text-sm">
      <strong>{{ Math.round(day.temp_max) }}°</strong>
      <span class="text-slate-400"> / {{ Math.round(day.temp_min) }}°</span>
    </span>
  </div>
</template>
