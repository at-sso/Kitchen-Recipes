// Function to fetch data from the '/result' route
function fetchData() {
  fetch("/results")
    .then((response) => response.json())
    .then((data) => {
      const responseGetter = document.getElementById("responseGetter");
      responseGetter.innerHTML = JSON.stringify(data, null, 2);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
      const responseGetter = document.getElementById("responseGetter");
      responseGetter.innerHTML = "Error fetching data. Please try again later.";
    });
}

// Call the fetchData function when the page loads
window.onload = fetchData;
