// Function to calculate the date 7 days from today
function calculateSevenDaysFromToday() {
    var today = new Date();
    var sevenDaysFromToday = new Date(today);
    sevenDaysFromToday.setDate(today.getDate() + 6);
    return sevenDaysFromToday.toISOString().split('T')[0];
}

// Set the min and max attributes for date input fields g
var dateInputs = document.querySelectorAll('input[type="date"]');
for (var i = 0; i < dateInputs.length; i++) {
    dateInputs[i].min = new Date().toISOString().split('T')[0]; // Set min to today
    dateInputs[i].max = calculateSevenDaysFromToday(); // Set max to 7 days from today
}
