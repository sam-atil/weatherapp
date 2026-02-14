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