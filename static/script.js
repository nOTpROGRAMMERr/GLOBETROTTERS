// script.js

function handleTravelTypeChange() {
  var travelTypeSelect = document.getElementById("travel_type");
  var adultsContainer = document.getElementById("adults_container");
  var childrenContainer = document.getElementById("children_container");
  var noAdultsSlider = document.getElementById("no_adults");
  var adultCountDisplay = document.getElementById("adult_count");
  var noChildrenSlider = document.getElementById("no_children");
  var childrenCountDisplay = document.getElementById("children_count");

  if (travelTypeSelect.value === "solo") {
    // Hide sliders and set displayed values to 0
    adultsContainer.classList.add("hidden");
    childrenContainer.classList.add("hidden");
    noAdultsSlider.value = 0;
    adultCountDisplay.textContent = 0;
    noChildrenSlider.value = 0;
    childrenCountDisplay.textContent = 0;
  } else {
    // Show sliders and update displayed values based on current slider positions
    adultsContainer.classList.remove("hidden");
    childrenContainer.classList.remove("hidden");
    adultCountDisplay.textContent = noAdultsSlider.value;
    childrenCountDisplay.textContent = noChildrenSlider.value;
  }
}

// Update displayed value when slider is moved (for adults)
noAdultsSlider.oninput = function() {
  adultCountDisplay.textContent = this.value;
}

// Update displayed value when slider is moved (for children)
noChildrenSlider.oninput = function() {
  childrenCountDisplay.textContent = this.value;
}

document.getElementById("itinerary_form").addEventListener("submit", function(event) {
    var generateButton = document.getElementById("generate_button");
    var loadingSpinner = document.getElementById("loading_spinner");

    // Hide the generate button and show the loading spinner
    generateButton.style.display = "none";
    loadingSpinner.style.display = "block";

    // You can perform additional actions here, such as submitting the form data
});
