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



/* Recipe carousel
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

 */

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
                <div class="card-header"><h4>${getCardTitle(cardDate)}</h4></div>
                <div class="card-body row">
                    <div class="col-md-3">
                        <h5 class="meal-title">Breakfast</h5>
                        <!-- Add recipe image and title here (if available) -->
                    </div>
                    <div class="col-md-3">
                        <h5 class="meal-title">Lunch</h5>
                        <!-- Add recipe image and title here (if available) -->
                    </div>
                    <div class="col-md-3">
                        <h5 class="meal-title">Dinner</h5>
                        <!-- Add recipe image and title here (if available) -->
                    </div>
                    <div class="col-md-3">
                        <h5 class="meal-title">Snack</h5>
                        <!-- Add recipe image and title here (if available) -->
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

