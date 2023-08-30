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

    var measurements = ["gr", "kg", "ml", "l", "tsp", "tbsp", "pcs", "pinch"];

    var measurementCol = document.createElement('div');
    measurementCol.classList.add('col');

    var measurementInput = document.createElement('select');
    measurementInput.classList.add('form-control');
    measurementInput.setAttribute('id', 'measurement-' + ingredientCounter);
    measurementInput.setAttribute('name', 'measurement-' + ingredientCounter);
    amountInput.required = true;

    for (const val of measurements) {
        var option = document.createElement("option");
        option.value = val;
        option.text = val.charAt(0) + val.slice(1);
        select.appendChild(option);
    }

    ingredientCol.appendChild(ingredientInput);
    amountCol.appendChild(amountInput);
    formRow.appendChild(ingredientCol);
    formRow.appendChild(amountCol);
    formRow.appendChild(measurementCol);

    ingredientFields.appendChild(formRow);

    ingredientCounter++;
});