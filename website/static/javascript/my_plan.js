//My_plan day cards
document.addEventListener('DOMContentLoaded', function () {

    const cardContainer = document.getElementById('card-container');
    

    // Get today's date
    const today = new Date();
    

    // Create cards for the next 7 days
    for (let i = 0; i < 7; i++) {
        const cardDate = new Date(today);
        cardDate.setDate(today.getDate() + i);

        const card = document.createElement('div');
        card.classList.add('mb-4');
        card.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h4>${getCardTitle(cardDate)}</h4>
                </div>
                <div class="card-body row">
                    <div class="col-md-3 plan-recipe-tile">
                        <h5 align="center"
                        class="meal-title"
                        id="breakfast-${cardDate}">
                        Breakfast</h5>   
                        ${getRecipeHTML('breakfast',
                            cardDate,
                            recipesJson,
                            myPlanRecipesJson)}
                    </div>
                    <div class="col-md-3 plan-recipe-tile">
                        <h5 align="center"
                        class="meal-title"
                        id="lunch-${cardDate}">
                        Lunch</h5>
                        ${getRecipeHTML('lunch',
                            cardDate,
                            recipesJson,
                            myPlanRecipesJson)}
                    </div>
                    <div class="col-md-3 plan-recipe-tile">
                        <h5 align="center"
                        class="meal-title"
                        id="dinner-${cardDate}">
                        Dinner</h5>
                        ${getRecipeHTML('dinner',
                            cardDate,
                            recipesJson,
                            myPlanRecipesJson)}
                    </div>
                    <div class="col-md-3 plan-recipe-tile">
                        <h5 align="center"
                        class="meal-title"
                        id="snack-${cardDate}">
                        Snack</h5>
                        ${getRecipeHTML('snack',
                            cardDate,
                            recipesJson,
                            myPlanRecipesJson)}
                    </div>
                </div>
            </div>
        `;

        // Create a new row for each card
        const cardRow = document.createElement('div');
        cardRow.classList.add('row', 'mb-4');
        cardRow.appendChild(card);

        // Append the row to the container
        cardContainer.appendChild(cardRow);
    }
});


function getRecipeHTML(mealName, cardDate, recipesJson, myPlanRecipesJson) {


    const matchingRecipe = myPlanRecipesJson.find(recipe => recipe.meal_name === mealName && formatDate(new Date(recipe.meal_date)) === formatDate(cardDate));

    if (matchingRecipe) {
        const recipeData = recipesJson.find(recipe => recipe.id === matchingRecipe.recipe_id);

            // Use recipeData to display the recipe information
            return `
                <div align="center" >
                    <div class="card mb-4 plan-recipe-tile recipe-tile mt-4">
                        <div class="card-body">
                            <img src="${recipeData.recipe_picture}" alt="Recipe Image" class="img-fluid">
                            <h6>${recipeData.title}</h6><br>
                            <button type="button" class="btn btn-outline-primary btn-sm mt-2" data-bs-toggle="modal" data-bs-target="#recipe-modal-${recipeData.id}">
                                View Recipe
                            </button>
                        </div>
                    </div>
                </div>
            `;
    } else {
        // No matching recipe in myPlanRecipesJson
        return `
            <div align="center" class="card text-white bg-secondary col-md-6 mx-auto mt-3">
                <h6>No entry</h6>
            </div>
        `;
    }
}

function getCardTitle(date) {
    if (isToday(date)) {
        return `Today - ${formatDate(date)}`;
    } else {
        return `${getDayOfWeek(date.getDay())} - ${formatDate(date)}`;
    }
}

function isToday(date) {
    const today = new Date();
    return date.toDateString() === today.toDateString();
}

function isSameDate(date1, date2) {
    return (
        date1.getDate() === date2.getDate() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getFullYear() === date2.getFullYear()
    );
}

function getDayOfWeek(dayIndex) {
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return daysOfWeek[dayIndex];
}

function formatDate(date) {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
}



//Search function for nutritionists on the My_Plan page
$(document).ready(function () {
    const searchInput = $("#search_input");
    const nutritionistCards = $(".nutritionist-card");

    searchInput.on("input", function () {
        const searchValue = searchInput.val().toLowerCase();

        nutritionistCards.each(function () {
            const nutritionistName = $(this).find(".nutritionist-name").text().toLowerCase();

            if (nutritionistName.includes(searchValue)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});