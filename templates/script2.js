function generateTravelItineraryPrompt(location, numberOfDays) {
    // Define a list of cities for suggestions
    const cities = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "San Diego",
        "Dallas",
        "San Jose",
        "Mumbai",
        "Pune",
        "Delhi"
    ];

    // Function to filter cities based on user input
    function filterCities(input) {
        return cities.filter(city =>
            city.toLowerCase().includes(input.toLowerCase())
        );
    }

    // Function to display city suggestions
    function displaySuggestions(suggestions) {
        const suggestionList = document.getElementById('suggestionList');
        suggestionList.innerHTML = ''; // Clear previous suggestions

        suggestions.forEach(city => {
            const li = document.createElement('li');
            li.textContent = city;
            suggestionList.appendChild(li);
        });
    }

    let prompt = `Generate a travel itinerary for a trip to ${location} for ${numberOfDays} days.\n\n`;
    console.log(prompt)

    for (let i = 1; i <= numberOfDays; i++) {
        prompt += `Day ${i}:\n`;
        // Add attractions for the day
        prompt += `- [ATTRACTION_${i}_1]: Visit [DESCRIPTION_${i}_1].\n`;
        prompt += `- [ATTRACTION_${i}_2]: Explore [DESCRIPTION_${i}_2].\n\n`;
    }

    prompt += `Additional Information:\n`;
    prompt += `- Accommodation: Stay at [HOTEL_NAME] in ${location}.\n`;
    prompt += `- Dining: Enjoy local cuisine at [RESTAURANT_1], [RESTAURANT_2], etc.\n`;
    prompt += `- Transportation: Use [TRANSPORTATION_MODE] for getting around.\n\n`;
    prompt += `Feel free to modify the prompt as needed for your specific use case, adding or removing details as desired.`;

    // Event listener for location input field
    document.getElementById('location').addEventListener('input', function() {
        const input = this.value.trim();
        const suggestions = filterCities(input);
        displaySuggestions(suggestions);
    });

    return prompt;
}
