import axios from 'axios'

// URL base del backend. Configurable con VITE_API_BASE_URL; por defecto, localhost.
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({ baseURL, timeout: 12000 })

/**
 * Consulta el clima actual + pronóstico de una ciudad al backend.
 * @param {string} city - Nombre de la ciudad.
 * @param {'metric'|'imperial'} units - Sistema de unidades.
 * @returns {Promise<object>} El objeto WeatherBundle ({ units, current, forecast }).
 */
export async function fetchWeather(city, units = 'metric') {
  const { data } = await api.get('/weather', { params: { city, units } })
  return data
}
