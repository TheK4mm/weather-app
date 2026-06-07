<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: { type: Object, required: true },
  units: { type: String, default: 'metric' },
})

const tempUnit = computed(() => (props.units === 'metric' ? '°C' : '°F'))
const windUnit = computed(() => (props.units === 'metric' ? 'm/s' : 'mph'))
</script>

<template>
  <section class="rounded-2xl bg-white/95 p-6 text-slate-800 shadow-xl">
    <header class="flex items-center justify-between gap-4">
      <div>
        <h2 class="text-2xl font-semibold">{{ data.city }}, {{ data.country }}</h2>
        <p class="capitalize text-slate-500">{{ data.description }}</p>
      </div>
      <img :src="data.icon" :alt="data.description" class="h-20 w-20 shrink-0" />
    </header>

    <div class="mt-2 flex items-end gap-2">
      <span class="text-6xl font-bold">{{ Math.round(data.temperature) }}</span>
      <span class="mb-2 text-2xl text-slate-500">{{ tempUnit }}</span>
    </div>

    <dl class="mt-4 grid grid-cols-3 gap-3 text-center text-sm">
      <div class="rounded-xl bg-slate-100 py-3">
        <dt class="text-slate-500">Sensación</dt>
        <dd class="font-semibold">{{ Math.round(data.feels_like) }}{{ tempUnit }}</dd>
      </div>
      <div class="rounded-xl bg-slate-100 py-3">
        <dt class="text-slate-500">Humedad</dt>
        <dd class="font-semibold">{{ data.humidity }}%</dd>
      </div>
      <div class="rounded-xl bg-slate-100 py-3">
        <dt class="text-slate-500">Viento</dt>
        <dd class="font-semibold">{{ data.wind_speed }} {{ windUnit }}</dd>
      </div>
    </dl>
  </section>
</template>
