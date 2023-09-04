document.addEventListener("DOMContentLoaded", function () {
    const editProfileBtn = document.getElementById("edit_profile_btn");
    const pfpForm = document.getElementById("pfp");
    const profileInfoForm = document.getElementById("profile_info");

    editProfileBtn.addEventListener("click", function () {
        pfpForm.style.display = "block"; // Show the profile picture form
        profileInfoForm.style.display = "block"; // Show the profile info form
    });
});


//Delete entries from the Nutritionist's information
$(document).ready(function () {
    $(".delete-btn").click(function () {
        const entryType = $(this).data("entry-type");
        const entryId = $(this).data("entry-id");

        let confirmationMessage = "";
        let deleteUrl = "";

        switch (entryType) {
            case "experience":
                confirmationMessage = "Are you sure you want to delete this entry?";
                deleteUrl = `/delete-experience/${entryId}`;
                break;
            case "education":
                confirmationMessage = "Are you sure you want to delete this entry?";
                deleteUrl = `/delete-education/${entryId}`;
                break;
            case "interest":
                confirmationMessage = "Are you sure you want to delete this entry?";
                deleteUrl = `/delete-interest/${entryId}`;
                break;
            default:
                return;
        }

        if (confirm(confirmationMessage)) {
            $.ajax({
                url: deleteUrl,
                type: "POST",
                success: function (response) {
                    // Reload the page after successful deletion
                    window.location.reload();
                },
                error: function () {
                    alert("An error occurred while deleting the entry.");
                }
            });
        }
    });
});

// Toggle the "Add recipe" form on the Nutritionist's profile
function toggleRecipeForm() {
    var form = document.getElementById("recipe-form");
    form.style.display = (form.style.display === "none") ? "block" : "none";
}

// Dynamically add Ingredient fields in the Recipe form and auto-complete them with database entries
document.addEventListener("DOMContentLoaded", function () {
    const ingredientFields = document.getElementById("ingredient-fields");
    const addIngredientButton = document.getElementById("add-ingredient");
    let fieldCounter = 1;

    addIngredientButton.addEventListener("click", function () {
        addIngredientFields();
    });

    function addIngredientFields() {
        const newIngredientField = document.createElement("div");
        newIngredientField.classList.add("form-group", "row");

        newIngredientField.innerHTML = `
            <div class="col-md-6" style="padding-right: 0;">
                <input type="text"
                    class="form-control ingredient"
                    name="ingredient[]"
                    id="ingredient-${fieldCounter}"
                    placeholder="Ingredient"
                    required
                    list="ingredient-suggestions-${fieldCounter}"
                />
                <datalist id="ingredient-suggestions-${fieldCounter}"></datalist>
            </div>
            <div class="col-md-3" style="padding-right: 0;">
                <input type="text" class="form-control amount" name="amount[]" placeholder="Amount" required>
            </div>
            <div class="form-group col-md-3">
                <select class="form-control measurement" name="measurement[]">
                    <option value="grams">gr</option>
                    <option value="kilograms">kg</option>
                    <option value="mililiters">ml</option>
                    <option value="liters">l</option>
                    <option value="teaspoon">tsp</option>
                    <option value="tablespoon">tbsp</option>
                    <option value="piece">pcs</option>
                    <option value="pinch">pinch</option>
                </select>
            </div>
        `;

        ingredientFields.appendChild(newIngredientField);

        fieldCounter++;

        // Set up auto-completion for the newly added ingredient field
        const newIngredientInput = newIngredientField.querySelector(".ingredient");
        setupIngredientAutoCompletion(newIngredientInput);
    }

    // Auto-completion for ingredient input fields
    function setupIngredientAutoCompletion(inputField) {
        inputField.addEventListener("input", function () {
            const inputText = inputField.value;

            if (inputText.length > 2) {
                fetch(`/get_ingredients?query=${inputText}`)
                    .then(response => response.json())
                    .then(data => {
                        const suggestions = data.ingredients;
                        displayIngredientSuggestions(inputField, suggestions);
                    })
                    .catch(error => console.error(error));
            }
        });
    }

    // Display ingredient suggestions as a datalist
    function displayIngredientSuggestions(inputField, suggestions) {
        const datalist = inputField.nextElementSibling;
        datalist.innerHTML = '';

        for (const suggestion of suggestions) {
            const option = document.createElement("option");
            option.value = suggestion;
            datalist.appendChild(option);
        }
    }

    // Set up auto-completion for existing ingredient fields
    const existingIngredientFields = document.querySelectorAll(".ingredient");
    existingIngredientFields.forEach(field => {
        setupIngredientAutoCompletion(field);
    });

});
