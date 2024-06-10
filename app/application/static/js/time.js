/* Display the current time on the chat page */

function updateTime() {
    const now = new Date();
    const timeElement = document.getElementById("time");
    timeElement.textContent = now.toLocaleTimeString();
  }
  
  setInterval(updateTime, 1000);
  
  $(document).ready(function() {
    // Get the current date
    var currentDate = new Date();

    // Format the date as desired (e.g., "MM/DD/YYYY")
    var formattedDate = (currentDate.getMonth() + 1) + "/" + currentDate.getDate() + "/" + currentDate.getFullYear();

    // Set the date value in the HTML element
    $("#date").text(formattedDate);
});
