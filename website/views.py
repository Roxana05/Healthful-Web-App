from click import DateTime
from flask import Blueprint, Request, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Nutritionist, Client, Notification, Recipe, Ingredient, Education, RelatedInterests, Experience, Afflictions, Medication, AllergiesIntolerances, Recommendation, RecipeIngredients , MyPlan, RecommendedRecipe, ClientWeight
from . import db
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime, date 

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'website/static/profile_pictures/'
RECIPE_UPLOAD_FOLDER = 'website/static/recipe_pictures/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@views.route('/client-profile', methods=['GET', 'POST'])
@login_required
def client_profile():
    client = Client.query.get(current_user.id)

    afflictions = Afflictions.query.filter_by(client_id=client.id).all();
    medications = Medication.query.filter_by(client_id=client.id).all();
    allergies = AllergiesIntolerances.query.filter_by(client_id=client.id).all();
    recommendations = Recommendation.query.filter_by(client_id=client.id).all();
    weights = ClientWeight.query.filter_by(client_id=client.id).all();
    meal_history = MyPlan.query.filter_by(client_id=client.id).all();
    meal_history.sort(key=lambda meal: meal.meal_date)
    meal_history.reverse()

    if request.method == 'POST' and 'height' in request.form:
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture and allowed_file(profile_picture.filename):
                filename = secure_filename(profile_picture.filename)
                profile_picture_path = os.path.join(UPLOAD_FOLDER, filename)
                profile_picture.save(profile_picture_path)
                client.profile_picture = filename
            else:
                flash('Invalid file format. Allowed formats are png, jpg, jpeg, gif', category='error')
        
        height = request.form.get('height')
        if height:
            client.height = float(height)

        weight = request.form.get('weight')
        if weight:
            client.weight = float(weight)
            current_weight = float(weight)
            weight_date = date.today()
            weight_entry = ClientWeight(client_id=client.id, recorded_weight=current_weight, weight_date=weight_date)

            db.session.add(weight_entry)

        if client.height and client.weight:
            bmi = round(client.weight/((client.height/100)**2), 2)
            client.bmi = bmi

        goal = request.form.get('goal')
        if goal:
            client.goal = goal

        desired_weight = request.form.get('desired-weight')
        if desired_weight:
            client.desired_weight = float(desired_weight)

        dd = request.form.get('desired-date')
        desired_date=datetime.strptime(dd, '%Y-%m-%d').date()
        if desired_date:
            client.desired_date = desired_date

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('views.client_profile'))

    elif request.method == 'POST' and 'new-affliction' in request.form:
        affliction = request.form.get('new-affliction')
        if affliction:
            new_affliction = Afflictions(client_id=current_user.id, affliction_name=affliction)
            db.session.add(new_affliction)
            db.session.commit()
            flash('Affliction entry added successfully!', 'success')
            return redirect(url_for('views.client_profile'))

    elif request.method == 'POST' and 'new-medication' in request.form:
        medication = request.form.get('new-medication')
        if medication:
            new_medication = Medication(client_id=current_user.id, medication_name=medication)
            db.session.add(new_medication)
            db.session.commit()
            flash('Medication entry added successfully!', 'success')
            return redirect(url_for('views.client_profile'))

    elif request.method == 'POST' and 'new-allergy' in request.form:
        allergy = request.form.get('new-allergy')
        if allergy:
            new_allergy = AllergiesIntolerances(client_id=current_user.id, allergy_name=allergy)
            db.session.add(new_allergy)
            db.session.commit()
            flash('Affliction entry added successfully!', 'success')
            return redirect(url_for('views.client_profile'))

    date_of_birth=client.date_of_birth

    today = datetime.now().date()
    age = None
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


    return render_template('client_profile.html', user=client, client=client, client_id=current_user.id, profile_picture=url_for('static', filename='profile_pictures/' + client.profile_picture), age=age, weights=weights, meal_history=meal_history, afflictions=afflictions, medications=medications, allergies=allergies, recommendations=recommendations)

@views.route('/my-plan', methods=['GET', 'POST'])
@login_required
def my_plan():
    nutritionists = Nutritionist.query.all()
    client = Client.query.get(current_user.id)
    experience_entries = Experience.query.all()
    education_entries = Education.query.all()
    interest_entries = RelatedInterests.query.all()
    recipes = Recipe.query.all()
    ingredients = Ingredient.query.all()
    recipe_ingredients = RecipeIngredients.query.all()
    my_plan_recipes = MyPlan.query.all()

    recipes_json = json.dumps([{
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'recipe_picture': recipe.recipe_picture,
    } for recipe in recipes])

    my_plan_recipes_json = json.dumps([{
        'client_id': current_user.id,
        'recipe_id': recipe.recipe_id,
        'meal_date': recipe.meal_date.strftime('%Y-%m-%d'),  # Convert date to string
        'meal_name': recipe.meal_name,
    } for recipe in my_plan_recipes])

    current_user_id_json = jsonify(current_user_id=current_user.id)

    if client.nutritionist_id:
        nutritionist = Nutritionist.query.get(client.nutritionist_id)
        experience_entries = Experience.query.filter_by(nutritionist_id=nutritionist.id).all()
        education_entries = Education.query.filter_by(nutritionist_id=nutritionist.id).all()
        interest_entries = RelatedInterests.query.filter_by(nutritionist_id=nutritionist.id).all()

        return render_template("my_plan.html", user=current_user, nutritionist=nutritionist, experience_entries=experience_entries, education_entries=education_entries, interest_entries=interest_entries, recipes=recipes, ingredients=ingredients, recipe_ingredients=recipe_ingredients, recipes_json=recipes_json, my_plan_recipes=my_plan_recipes, my_plan_recipes_json=my_plan_recipes_json)
    return render_template("my_plan.html", user=current_user, nutritionists=nutritionists, experience_entries=experience_entries, education_entries=education_entries, interest_entries=interest_entries, recipes=recipes, ingredients=ingredients, recipe_ingredients=recipe_ingredients, recipes_json=recipes_json, my_plan_recipes=my_plan_recipes, my_plan_recipes_json=my_plan_recipes_json)

@views.route('/recipes', methods=['GET', 'POST'])
@login_required
def recipes():
    user = User.query.filter_by(id=current_user.id).first()
    recipes = Recipe.query.all()
    ingredients = Ingredient.query.all()
    recipe_ingredients = RecipeIngredients.query.all()

    breakfast_recipes = Recipe.query.filter_by(recipe_type="breakfast")
    main_recipes = Recipe.query.filter_by(recipe_type="main")
    snack_recipes = Recipe.query.filter_by(recipe_type="snack")
   
    if user.account_type == 'nutritionist':
        clients = user.clients

        if request.method == 'POST':
            recipe_id = request.form.get('recipe_id')
            client_id = request.form.get('client_id')

            # Create a new entry in the RecommendedRecipe table.
            recommended_recipe = RecommendedRecipe(client_id=client_id, recipe_id=recipe_id)
            db.session.add(recommended_recipe)
            db.session.commit()

            flash('Recipe recommended!', 'success')
            return redirect(url_for('views.recipes'))

        return render_template("recipes.html", user=current_user, clients=clients, recipes=recipes, breakfast_recipes=breakfast_recipes, main_recipes=main_recipes, snack_recipes=snack_recipes, ingredients=ingredients, recipe_ingredients=recipe_ingredients)
    
    else:
        recommended_recipes = RecommendedRecipe.query.filter_by(client_id=current_user.id).all()
        return render_template("recipes.html", user=current_user, recipes=recipes, breakfast_recipes=breakfast_recipes, main_recipes=main_recipes, snack_recipes=snack_recipes, ingredients=ingredients, recipe_ingredients=recipe_ingredients, recommended_recipes=recommended_recipes)

    return render_template("recipes.html", user=current_user, recipes=recipes, ingredients=ingredients, recipe_ingredients=recipe_ingredients)

@views.route('/client-list', methods=['GET', 'POST'])
@login_required
def client_list():
    clients = Client.query.filter_by(nutritionist_id=current_user.id).all()
    return render_template("client_list.html", user=current_user, clients=clients)

@views.route('/client-record/<client_id>', methods=['GET', 'POST'])
@login_required
def client_record(client_id):
    client = Client.query.filter_by(id=client_id).first()
    user = User.query.get(current_user.id)

    afflictions = Afflictions.query.filter_by(client_id=client.id).all();
    medications = Medication.query.filter_by(client_id=client.id).all();
    allergies = AllergiesIntolerances.query.filter_by(client_id=client.id).all();
    recommendations = Recommendation.query.filter_by(client_id=client.id).all();
    weights = ClientWeight.query.filter_by(client_id=client.id).all();
    meal_history = MyPlan.query.filter_by(client_id=client.id).all();
    meal_history.sort(key=lambda meal: meal.meal_date)
    meal_history.reverse()

    today = datetime.now().date()
    client_age = None
    client_age = today.year - client.date_of_birth.year - ((today.month, today.day) < (client.date_of_birth.month, client.date_of_birth.day))

    if request.method == 'POST' and 'new-general-input' in request.form:
        general_recommendation = request.form.get('new-general-input')
        if general_recommendation:
            new_general_recommendation = Recommendation(nutritionist_id=current_user.id, client_id=client_id, rec_category="general", content=general_recommendation)
            db.session.add(new_general_recommendation)
            db.session.commit()
            flash('Recommendation added successfully!', 'success')
            return redirect(url_for('views.client_record', client_id=client.id))

    if request.method == 'POST' and 'new-practical-input' in request.form:
        practical_recommendation = request.form.get('new-practical-input')
        if practical_recommendation:
            new_practical_recommendation = Recommendation(nutritionist_id=current_user.id, client_id=client_id, rec_category="practical", content=practical_recommendation)
            db.session.add(new_practical_recommendation)
            db.session.commit()
            flash('Recommendation added successfully!', 'success')
            return redirect(url_for('views.client_record', client_id=client.id))
            
    if request.method == 'POST' and 'new-physical-input' in request.form:
        physical_recommendation = request.form.get('new-physical-input')
        if physical_recommendation:
            new_physical_recommendation = Recommendation(nutritionist_id=current_user.id, client_id=client_id, rec_category="physical", content=physical_recommendation)
            db.session.add(new_physical_recommendation)
            db.session.commit()
            flash('Recommendation added successfully!', 'success')
            return redirect(url_for('views.client_record', client_id=client.id))

    if request.method == 'POST' and 'breakfast-input' in request.form:
        breakfast_calories = request.form.get('breakfast-input')
        lunch_calories = request.form.get('lunch-input')
        dinner_calories = request.form.get('dinner-input')
        snack_calories = request.form.get('snack-input')

        client.breakfast_calories = breakfast_calories
        client.lunch_calories = lunch_calories
        client.dinner_calories = dinner_calories
        client.snack_calories = snack_calories

        db.session.commit()
        flash('Meal plan updated successfully!', category='success')
        return redirect(url_for('views.client_record', client_id=client.id))

    return render_template("client_record.html", nutritionist=user, client=client, client_age=client_age, weights=weights, meal_history=meal_history, afflictions=afflictions, medications=medications, allergies=allergies, recommendations=recommendations)
   
@views.route('/meal_plan', methods=['GET', 'POST'])
@login_required
def meal_plan():
    user = User.query.get(current_user.id)
    if user.account_type == 'client':
        client = Client.query.get(current_user.id)

    if user.account_type == 'nutritionist':
        return render_template("meal_plan.html", nutritionist=user, client=client)
    
    return render_template("meal_plan.html", client=client)

@views.route('/nutritionist-profile', methods=['GET', 'POST'])
@login_required
def nutritionist_profile():
    nutritionist = Nutritionist.query.get(current_user.id)
    experience_entries = Experience.query.filter_by(nutritionist_id=nutritionist.id).all()
    education_entries = Education.query.filter_by(nutritionist_id=nutritionist.id).all()
    interest_entries = RelatedInterests.query.filter_by(nutritionist_id=nutritionist.id).all()
    ingredients = Ingredient.query.all()

    if request.method == 'POST':
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture and allowed_file(profile_picture.filename):
                filename = secure_filename(profile_picture.filename)
                profile_picture_path = os.path.join(UPLOAD_FOLDER, filename)
                profile_picture.save(profile_picture_path)
                nutritionist.profile_picture = filename
            else:
                flash('Invalid file format. Allowed formats are png, jpg, jpeg, gif', category='error')

            db.session.commit()
            flash('Profile updated successfully!', category='success')
            return redirect(url_for('views.nutritionist_profile'))

        elif request.method == 'POST' and 'address' in request.form:
            address = request.form.get('address')
            if address:
                nutritionist.address = address

            city = request.form.get('city')
            if city:
                nutritionist.city = city

            country = request.form.get('country')
            if country:
                nutritionist.country = country

            phone_number = request.form.get('phone_number')
            if phone_number:
                nutritionist.phone_number = phone_number

            description = request.form.get('description')
            if description:
                nutritionist.description = description


            db.session.commit()
            flash('Profile updated successfully!', category='success')
            return redirect(url_for('views.nutritionist_profile'))

        elif request.method == 'POST' and 'job' in request.form:
            job = request.form.get('job')
            company = request.form.get('company')
            job_description = request.form.get('job-description')
            job_start_year = int(request.form.get('job-start-year'))
            job_end_year = int(request.form.get('job-end-year'))

            if nutritionist:
                 new_experience = Experience(
                                  nutritionist_id=nutritionist.id,
                                  job=job,
                                  company=company,
                                  job_description=job_description,
                                  job_start_year=job_start_year,
                                  job_end_year=job_end_year
                                  )
                 db.session.add(new_experience)
                 db.session.commit()
                 flash('Experience entry added successfully!', 'success')
                 return redirect(url_for('views.nutritionist_profile'))

        elif request.method == 'POST' and 'school' in request.form:
            school = request.form.get('school')
            degree = request.form.get('degree')
            field_of_study = request.form.get('field-of-study')
            education_start_year = int(request.form.get('education-start-year'))
            education_end_year = int(request.form.get('education-end-year'))

            if nutritionist:
                 new_education = Education(
                                  nutritionist_id=nutritionist.id,
                                  school=school,
                                  degree=degree,
                                  field_of_study=field_of_study,
                                  education_start_year=education_start_year,
                                  education_end_year=education_end_year
                                  )
                 db.session.add(new_education)
                 db.session.commit()
                 flash('Education entry added successfully!', 'success')
                 return redirect(url_for('views.nutritionist_profile'))

        elif request.method == 'POST' and 'interest' in request.form:
            interest = request.form.get('interest')
            interest_description = request.form.get('interest-description')

            if nutritionist:
                 new_interest = RelatedInterests(
                                  nutritionist_id=nutritionist.id,
                                  interest=interest,
                                  interest_description=interest_description
                                  )

                 db.session.add(new_interest)
                 db.session.commit()
                 flash('Interest entry added successfully!', 'success')
                 return redirect(url_for('views.nutritionist_profile'))

        elif request.method == 'POST' and 'recipe-type' in request.form:
            title = request.form.get('title')
            recipe_type = request.form.get('recipe-type')
            description = request.form.get('description')
        
            ingredient_names = request.form.getlist('ingredient[]')
            ingredient_amounts = request.form.getlist('amount[]')
            ingredient_measurements = request.form.getlist('measurement[]')

            ingr_names = ingredient_names
            ingr_amounts = ingredient_amounts
            ingr_measurements = ingredient_measurements

            ingredient_data = list(zip(ingredient_names, ingredient_amounts, ingredient_measurements))

            total_recipe_calories = 0
            total_recipe_proteins = 0
            total_recipe_carbs = 0
            total_recipe_fats = 0

            for index, name in enumerate(ingr_names):
                amount = ingr_amounts[index]
                measurement = ingr_measurements[index]

                if measurement == "kg" or measurement == "l":
                    amount = amount * 1000
                elif measurement == "tbsp":
                    amount = amount * 14;
                elif measurement == "tsp":
                    amount = amount * 6;

                amount = float(amount)

                ingredient = Ingredient.query.filter_by(name=name).first()

                calories = float(ingredient.calories)
                proteins = float(ingredient.proteins)
                carbs = float(ingredient.carbs)
                fats = float(ingredient.fats)

                total_ingr_calories = (amount * calories) / 100
                total_ingr_proteins = (amount * proteins) / 100
                total_ingr_carbs = (amount * carbs) / 100
                total_ingr_fats = (amount * fats) / 100

                total_recipe_calories += total_ingr_calories
                total_recipe_proteins += total_ingr_proteins
                total_recipe_carbs += total_ingr_carbs
                total_recipe_fats += total_ingr_fats

            total_recipe_calories = "{:.2f}".format(total_recipe_calories)
            total_recipe_proteins = "{:.2f}".format(total_recipe_proteins / 1000)
            total_recipe_carbs = "{:.2f}".format(total_recipe_carbs / 1000)
            total_recipe_fats = "{:.2f}".format(total_recipe_fats / 1000)

            recipe_picture = request.files['recipe-picture'] if 'recipe-picture' in request.files else None

            add_recipe_to_db(title, recipe_type, description, total_recipe_calories, total_recipe_proteins, total_recipe_carbs, total_recipe_fats, ingredient_data, recipe_picture)
        
            flash('Recipe added successfully!', category='success')
            return redirect(url_for('views.nutritionist_profile'))  # Redirect back to the profile page

    return render_template('nutritionist_profile.html', user=nutritionist, profile_picture=url_for('static', filename='profile_pictures/' + nutritionist.profile_picture), experience_entries=experience_entries, education_entries=education_entries, interest_entries=interest_entries, ingredients=ingredients)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# NOTIFICATION SECTION
@views.route('/send-request/<int:nutritionist_id>', methods=['POST'])
def send_request(nutritionist_id):
   nutritionist = Nutritionist.query.get(nutritionist_id)
   response_data = {'success': False}

   if current_user.nutritionist_id:
        response_data['message'] = 'You have already registered to a nutritionist'
   else:
        if nutritionist:
            send_notification(nutritionist.id)
            response_data['success'] = True
            response_data['message'] = 'Request sent!'
        else:
            response_data['message'] = 'Nutritionist not found.'

   flash(response_data['message'], 'success' if response_data['success'] else 'error')

   return redirect(url_for('views.my_plan'))

def send_notification(nutritionist_id):
    nutritionist = Nutritionist.query.get(nutritionist_id)
    if nutritionist:
        notification = Notification(
            message="You have a new request from a client.",
            client_id=current_user.id,
            nutritionist_id=nutritionist.id,
            status='pending'
        )
        db.session.add(notification)
        db.session.commit()

@views.route('/accept-request/<int:notification_id>', methods=['POST'])
def accept_request(notification_id):
    notification = Notification.query.get(notification_id)
    if notification:

        # Update the status of the notification
        notification.status = 'accepted'

        #Add the nutritionist's id in the client's db and the client's id to the nutritionist's list
        client = notification.client
        nutritionist = notification.nutritionist

        client.nutritionist_id = nutritionist.id
        nutritionist.clients.append(client)

        db.session.commit()

         # Send a notification to the client
        send_notification_to_client(notification.client_id, "Your request has been accepted.")


        flash('Client added successfully!', 'success')

    return redirect(url_for('views.client_list'))

@views.route('/decline-request/<int:notification_id>', methods=['POST'])
def decline_request(notification_id):
    notification = Notification.query.get(notification_id)
    if notification:
        # Update the status of the notification
        notification.status = 'declined'
        db.session.commit()
        
        # Send a notification to the client
        send_notification_to_client(notification.client_id, "Your request has been declined.")


    return redirect(url_for('views.client_list'))

def send_notification_to_client(client_id, message):
    notification = Notification(
        message=message,
        client_id=client_id,
        nutritionist_id=current_user.id,
        status='notification'  # You can define a custom status for notifications
    )
    db.session.add(notification)
    db.session.commit()




@views.route('/delete-affliction/<int:affliction_id>', methods=['POST'])
@login_required
def delete_affliction(affliction_id):
    affliction = Afflictions.query.get(affliction_id)
    
    if affliction:
        db.session.delete(affliction)
        db.session.commit()
        flash('Affliction deleted successfully!', 'success')
    else:
        flash('Affliction not found.', 'error')

    return redirect(url_for('views.client_profile'))

@views.route('/delete-medication/<int:medication_id>', methods=['POST'])
@login_required
def delete_medication(medication_id):
    medication = Medication.query.get(medication_id)
    
    if medication:
        db.session.delete(medication)
        db.session.commit()
        flash('Medication deleted successfully!', 'success')
    else:
        flash('Medication not found.', 'error')

    return redirect(url_for('views.client_profile'))

@views.route('/delete-allergy/<int:allergy_id>', methods=['POST'])
@login_required
def delete_allergy(allergy_id):
    allergy = AllergiesIntolerances.query.get(allergy_id)
    
    if allergy:
        db.session.delete(allergy)
        db.session.commit()
        flash('Allergy deleted successfully!', 'success')
    else:
        flash('Allergy not found.', 'error')

    return redirect(url_for('views.client_profile'))

@views.route('/delete-recommendation/<int:client_id>/<int:recommendation_id>', methods=['POST'])
@login_required
def delete_recommendation(client_id, recommendation_id):
    recommendation = Recommendation.query.get(recommendation_id)
    
    if recommendation:
        db.session.delete(recommendation)
        db.session.commit()
        flash('Recommendation deleted successfully!', 'success')
    else:
        flash('Recommendation not found.', 'error')

    return redirect(url_for('views.client_record', client_id=client_id))

@views.route('/delete-experience/<int:entry_id>', methods=['POST'])
@login_required
def delete_experience(entry_id):
    experience = Experience.query.get(entry_id)
    
    if experience:
        db.session.delete(experience)
        db.session.commit()
        flash('Entry deleted successfully!', 'success')
    else:
        flash('Entry not found.', 'error')

    return redirect(url_for('views.nutritionist_profile'))

@views.route('/delete-education/<int:entry_id>', methods=['POST'])
@login_required
def delete_education(entry_id):
    education = Education.query.get(entry_id)
    
    if education:
        db.session.delete(education)
        db.session.commit()
        flash('Entry deleted successfully!', 'success')
    else:
        flash('Entry not found.', 'error')

    return redirect(url_for('views.nutritionist_profile'))

@views.route('/delete-interest/<int:entry_id>', methods=['POST'])
@login_required
def delete_interest(entry_id):
    interest = RelatedInterests.query.get(entry_id)
    
    if interest:
        db.session.delete(interest)
        db.session.commit()
        flash('Entry deleted successfully!', 'success')
    else:
        flash('Entry not found.', 'error')

    return redirect(url_for('views.nutritionist_profile'))



# RECIPE SECTION

# Ingredient auto-complete
@views.route('/get_ingredients')
def get_ingredients():
    query = request.args.get('query', '')

    ingredients = Ingredient.query.filter(Ingredient.name.startswith(query)).limit(20).all()

    suggestions = [ingredient.name for ingredient in ingredients]
    return jsonify({'ingredients': suggestions})

# Add recipe to the database
def add_recipe_to_db(title, recipe_type, description, total_recipe_calories, total_recipe_proteins, total_recipe_carbs, total_recipe_fats, ingredient_data, picture=None):
    # Create a new Recipe object and populate its attributes
    new_recipe = Recipe(
        title=title,
        recipe_type=recipe_type,
        description=description,
        total_calories=total_recipe_calories,
        total_proteins=total_recipe_proteins, 
        total_carbs=total_recipe_carbs,
        total_fats=total_recipe_fats,
    )

    if picture:
        if allowed_file(picture.filename):
            filename = secure_filename(picture.filename)
            picture_path = os.path.join(RECIPE_UPLOAD_FOLDER, filename)
            picture.save(picture_path)
            new_recipe.recipe_picture = filename
        else:
            flash('Invalid file format. Allowed formats are png, jpg, jpeg, gif', category='error')
            return  # Stop processing if the picture is not valid

    # Add the new recipe to the database
    db.session.add(new_recipe)
    db.session.commit()

    # Loop through the ingredient data and add to the RecipeIngredients table
    for name, amount, measurement in ingredient_data:
        ingredient = Ingredient.query.filter_by(name=name).first()
        if not ingredient:
            flash(f"Ingredient '{name}' is not available in the database.", category='error')
            return  # Stop processing if the ingredient doesn't exist in the database

        recipe_ingredient = RecipeIngredients(
            recipe_id=new_recipe.id,
            ingredient_id=ingredient.id,
            ingredient_name=ingredient.name,
            amount=float(amount),
            measurement=measurement
        )
        db.session.add(recipe_ingredient)



    db.session.commit()
    return redirect(url_for('views.nutritionist_profile'))

# Add recipe to My Plan
@views.route('/save_to_myplan', methods=['POST'])
def save_to_myplan():
    if request.method == 'POST':

        recipe_id = int(request.form['recipe_id'])
        meal_date = request.form.get('meal-date')
        date = datetime.strptime(meal_date, '%Y-%m-%d').date()
        meal_name = request.form.get('meal-type')
        client_id = current_user.id  # Replace with how you get the current user's ID

        # Create a new MyPlan entry and save it to the database
        my_plan_entry = MyPlan(client_id=client_id,
                              recipe_id=recipe_id, 
                              meal_date=date,
                             meal_name=meal_name)
        db.session.add(my_plan_entry)
        db.session.commit()

        flash('Recipe added to My Plan successfully!', 'success')
        return redirect(url_for('views.recipes'))

# MY PLAN SECTION
# Remove recipes from My Plan
@views.route('/delete_myplan_entry/<int:entry_id>', methods=['POST'])
def delete_myplan_entry(entry_id):
    entry_to_delete = MyPlan.query.get(entry_id)
    if entry_to_delete:
        db.session.delete(entry_to_delete)
        db.session.commit()
        flash('Entry deleted successfully', 'success')
    else:
        flash('Entry not found', 'error')
    
    return redirect(url_for('views.my_plan'))
