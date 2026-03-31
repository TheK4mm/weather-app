const API_KEY = "c4ca19936fb749869bb145417251410";

async function buscarClima() {
  const ciudad = document.getElementById("ciudad").value.trim();
  const resultado = document.getElementById("resultado");
  const errorDiv = document.getElementById("error");
  resultado.innerHTML = "";
  errorDiv.textContent = "";

  if (!ciudad) {
    errorDiv.textContent = "Por favor, escribe una ciudad.";
    return;
  }

  try {
    const url = `https://api.weatherapi.com/v1/current.json?key=${API_KEY}&q=${encodeURIComponent(ciudad)}&lang=es`;
    const respuesta = await fetch(url);
    const datos = await respuesta.json();

    if (datos.error) {
      errorDiv.textContent = "No se encontró la ciudad.";
      return;
    }

    resultado.innerHTML = `
      <h2>${datos.location.name}, ${datos.location.country}</h2>
      <img src="https:${datos.current.condition.icon}" alt="icono del clima">
      <p><strong>${datos.current.temp_c}°C</strong></p>
      <p>${datos.current.condition.text}</p>
    `;
  } catch (error) {
    errorDiv.textContent = "Hubo un problema con la conexión...";
  }
}
