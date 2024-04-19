// Function to fetch and display recipes
function viewRecipes() {
  fetch("/view")
    .then((response) => response.json())
    .then((recipes) => {
      const recipesContainer = document.getElementById("recipesContainer");
      recipesContainer.innerHTML =
        "<pre>" + JSON.stringify(recipes, null, 2) + "</pre>";
    });
}

// Update recipes dynamically when the page loads
viewRecipes();

// Event listener for the add form submission
document.getElementById("addForm").addEventListener("submit", function (event) {
  event.preventDefault();
  const formData = new FormData(this);
  fetch("/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      viewRecipes();
    });
});

// Event listener for the update form submission
document
  .getElementById("updateForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch("/update", {
      method: "PUT",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        viewRecipes();
      });
  });

// Event listener for the delete form submission
document
  .getElementById("deleteForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch("/delete", {
      method: "DELETE",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        viewRecipes();
      });
  });
