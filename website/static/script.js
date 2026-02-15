//Gathering info from form
const form = document.getElementById("weather_form")

if (form) {
    form.addEventListener("submit", async function (event){
        event.preventDefault(); //Prevents reload

        const city = document.getElementById("city").value.trim();
        const state = document.getElementById("state").value.trim();
        const country = document.getElementById("country").value.trim();

        //If any field is empty
        if (!city || !state || !country) {
            document.getElementById("error").textContent = "A field is missing";
            return;
        }

        //Fetch API Route from Views.py
        const response = await fetch("/api/v1/weather", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ city, state, country})
        });

        //If Response returned is valid, otherwise user submitted incorrect info
        if (response.ok) {
            window.location.href = "/dashboard"; //Calling on dashboard route
        }
        else {
            document.getElementById("error").textContent = "Invalid inputs";
        }

    });
}


//Rendering on Dashboard
async function displayWeather(){
    const container = document.getElementById("weather");

    if (!container) return;

    const response = await fetch("/api/v1/display");

    if (!response.ok) {
        container.textContent = "No Weather data"
        return;
    }

    const data = await response.json();
    const temp = data.main.temp;
    const humidity = data.main.humidity;
    const dewPoint = temp - ((100 - humidity) / 5)
    container.innerHTML = `
        <div class="card border-0 card-color">
            <div class="card-body">

                <!-- Header -->
                <div>
                    <h5 class="text-uppercase text-light text-bold mb-3">Current weather</h6>
                    <small>${new Date(data.dt * 1000).toLocaleString()}</small>
                </div>

                <!-- Main row -->
                <div class="row align-items-center">

                    <!-- Icon -->
                    <div class="col-md-2 text-center">
                        <img src="https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png" class = "weather-img">
                    </div>

                    <!-- Temperature -->
                    <div class="col-md-4">
                        <h1 class="display-2 mb-0 text-light">${Math.round(temp)}°C</h1>
                    </div>

                    <!-- Condition -->
                    <div class="col-md-6">
                        <h4 class="mb-1 text-light">${data.weather[0].main}</h4>
                        <p>Feels like ${Math.round(data.main.feels_like)}°C</p>
                    </div>

                </div>

                <!-- Description Row -->
                <div class = "row">
                    <p class="mt-1 mb-4">
                        The skies will be ${data.weather[0].description}.
                    </p>
                </div>

                <!-- Stats row -->
                <div class="row text-center">

                    <div class="col-2">
                        <div class="p-1 border rounded">
                            <h6 class = "text-light">Wind</h6>
                            <p>${data.wind.speed} km/h</p>
                        </div>
                    </div>

                    <div class="col-2">
                        <div class="p-1 border rounded">
                            <h6 class = "text-light">Humidity</h6>
                            <p>${humidity}%</p>
                        </div>
                    </div>

                    <div class="col-2">
                        <div class="p-1 border rounded">
                            <h6 class = "text-light">Visibility</h6>
                            <p>${(data.visibility/1000)} km</p>
                        </div>
                    </div>

                    <div class="col-2">
                        <div class="p-1 border rounded">
                            <h6 class = "text-light">Pressure</h6>
                            <p>${data.main.pressure} mb</p>
                        </div>
                    </div>

                    <div class="col-2">
                        <div class="p-1 border rounded">
                            <h6 class = "text-light">Dew point</h6>
                            <p>${dewPoint.toFixed(1)}°C</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;

}

document.addEventListener("DOMContentLoaded", displayWeather);