$(document).ready(function () {
    // Handle the accept button click event
    $("#acceptButton").click(function () {
        var clientId = $("#clientID").val();
        var nutritionistId = $("#nutritionistID").val();

        $.ajax({
            url: '/accept_request',
            type: 'POST',
            data: { 'client_id': clientId, 'nutritionist_id': nutritionistId },
            success: function (response) {
                alert('Request accepted');
                location.reload(); // Refresh the page or perform any other desired action
            },
            error: function (error) {
                alert('Error accepting request');
            }
        });
    });

    // Handle the reject button click event
    $("#rejectButton").click(function () {
        var clientId = $("#clientID").val();
        var nutritionistId = $("#nutritionistID").val();

        $.ajax({
            url: '/reject_request',
            type: 'POST',
            data: { 'client_id': clientId, 'nutritionist_id': nutritionistId },
            success: function (response) {
                alert('Request rejected');
                location.reload(); // Refresh the page or perform any other desired action
            },
            error: function (error) {
                alert('Error rejecting request');
            }
        });
    });
});


//Toggle the "Add recipe" form on the Nutritionist's profile
$(document).ready(function () {
    $("#edit_profile_btn").click(function () {
        $("#profile_info, #pfp").toggle();
    });
});

function toggleRecipeForm() {
    var form = document.getElementById("recipe-form");
    form.style.display = (form.style.display === "none") ? "block" : "none";
}


// Dinamically add ingredients for a recipe
var ingredientCounter = 2;

// Add ingredient fields dynamically
document.getElementById('add-ingredient').addEventListener('click', function () {
    var ingredientFields = document.getElementById('ingredient-fields');

    var formRow = document.createElement('div');
    formRow.classList.add('form-row', 'mt-2');

    var ingredientCol = document.createElement('div');
    ingredientCol.classList.add('col');

    var ingredientInput = document.createElement('input');
    ingredientInput.setAttribute('type', 'text');
    ingredientInput.classList.add('form-control');
    ingredientInput.setAttribute('id', 'ingredient-' + ingredientCounter);
    ingredientInput.setAttribute('name', 'ingredient-' + ingredientCounter);
    ingredientInput.setAttribute('placeholder', 'Ingredient');
    ingredientInput.required = true;

    var amountCol = document.createElement('div');
    amountCol.classList.add('col');

    var amountInput = document.createElement('input');
    amountInput.setAttribute('type', 'text');
    amountInput.classList.add('form-control');
    amountInput.setAttribute('id', 'amount-' + ingredientCounter);
    amountInput.setAttribute('name', 'amount-' + ingredientCounter);
    amountInput.setAttribute('placeholder', 'Amount');
    amountInput.required = true;

    ingredientCol.appendChild(ingredientInput);
    amountCol.appendChild(amountInput);
    formRow.appendChild(ingredientCol);
    formRow.appendChild(amountCol);

    ingredientFields.appendChild(formRow);

    ingredientCounter++;
});


// Recipe carousel
var carouselElement = document.getElementById("breakfast-carousel");
var carouselItems = carouselElement.querySelectorAll(".carousel-item");
var visible_items;

function updateVisibleItems() {
    if (window.innerWidth < 576) {
        visible_items = 1;
    } else if (window.innerWidth < 992) {
        visible_items = 2;
    } else {
        visible_items = 4;
    }

    for (var i = 0; i < carouselItems.length; i++) {
        carouselItems[i].classList.remove("active");
        carouselItems[i].querySelector(".row").innerHTML = "";
    }

    for (var j = 0; j < carouselItems.length; j += visible_items) {
        carouselItems[j].classList.add("active");
        var startIndex = j;
        var endIndex = j + visible_items;
        var items = Array.prototype.slice.call(carouselItems, startIndex, endIndex);

        for (var k = 0; k < items.length; k++) {
            var item = items[k];
            var recipeTiles = item.querySelectorAll(".recipe-tile");

            for (var l = 0; l < recipeTiles.length; l++) {
                var recipeTile = recipeTiles[l];
                item.querySelector(".row").appendChild(recipeTile);
            }
        }
    }
}

updateVisibleItems();

window.addEventListener("resize", function () {
    updateVisibleItems();
});
