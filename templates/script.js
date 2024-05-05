// // Helper functions
// const getFormData = () => {
//   const formData = new FormData(form);
//   const data = {};
//   for (const [key, value] of formData.entries()) {
//     data[key] = value;
//   }
//   return data;
// };
//
// const isValidForm = (formData) => {
//   const { location, from_loc } = formData;
//   if (!location || !from_loc) {
//     alert('Please enter a location and starting point.');
//     return false;
//   }
//   return true;
// };
//
// const handleSubmit = async (event) => {
//   event.preventDefault();
//
//   const formData = getFormData();
//   if (!isValidForm(formData)) {
//     return;
//   }
//
// //   try {
// //     // Simulate form submission with provided data (for testing purposes)
// //     const { location, from_loc } = formData;
// //     if (location === 'New York' && from_loc === 'Los Angeles') {
// //       window.location.href = 'page2.html';
// //     } else {
// //       throw new Error('Invalid form data. Please try again.');
// //     }
// //   } catch (error) {
// //     alert(error.message);
// //   } finally {
// //     hideSpinner();
// //   }
// // };
//
//
// const handleTravelTypeChange = () => {
//   const travelType = document.getElementById('travel_type').value;
//   const adultsContainer = document.getElementById('adults_container');
//   const childrenContainer = document.getElementById('children_container');
//
//   if (travelType === 'solo') {
//     adultsContainer.classList.add('hidden');
//     childrenContainer.classList.add('hidden');
//   } else {
//     adultsContainer.classList.remove('hidden');
//     childrenContainer.classList.remove('hidden');
//   }
// };
//
//
//
//
// const updateTravelerCount = (type, value) => {
//   const counterElement = document.getElementById(`${type}_count`);
//   counterElement.textContent = value;
// };
//
// const showSpinner = () => {
//   spinner.classList.add('show-spinner');
// };
//
// const hideSpinner = () => {
//   spinner.classList.remove('show-spinner');
// };
//
// // Event listeners
// const form = document.querySelector('form');
// const spinner = document.querySelector('#loading_spinner');
// const submitButton = document.querySelector('button[type="submit"]');
//
// form.addEventListener('submit', handleSubmit);
// submitButton.addEventListener('click', showSpinner);
//
// document.getElementById('no_adults').addEventListener('input', (event) => {
//   updateTravelerCount('adult', event.target.value);
// });
//
// document.getElementById('no_children').addEventListener('input', (event) => {
//   updateTravelerCount('children', event.target.value);
// });
//
// document.getElementById('travel_type').addEventListener('change', handleTravelTypeChange);
//
// // Hide the spinner initially
// hideSpinner();
// }
//
