from flask import Blueprint, Request, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Nutritionist, Client, Recipe, Ingredient
from . import db
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'website/static/profile_pictures/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/client-profile', methods=['GET', 'POST'])
@login_required
def client_profile():
    client = Client.query.get(current_user.id)

    if request.method == 'POST':
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture and allowed_file(profile_picture.filename):
                filename = secure_filename(profile_picture.filename)
                profile_picture_path = os.path.join(UPLOAD_FOLDER, filename)
                profile_picture.save(profile_picture_path)
                client.profile_picture = filename
            else:
                flash('Invalid file format. Allowed formats are png, jpg, jpeg, gif', category='error')
        
        print(profile_picture)

        height = request.form.get('height')
        if height:
            client.height = float(height)

        weight = request.form.get('weight')
        if weight:
            client.weight = float(weight)

        if client.height and client.weight:
            bmi = round(client.weight/((client.height/100)**2), 2)
            client.bmi = bmi

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('views.client_profile'))


    def send_request():
        if request.method == 'POST':
            nutritionist_email = request.form.get('nutritionist_email')

            nutritionist = Nutritionist.query.filter_by(email=nutritionist_email).first()

            #Check if the Nutritionist is already registered
            if current_user.nutritionist_id == nutritionist.id:
                flash('Nutritionist already added', 'info')

            #Check if the email address is registered as a Nutritionist
            if nutritionist:                                
                #send_notification(nutritionist.email, current_user.id)
                flash('Request sent!', category='success')
            else:
                flash("Nutritionist not found.", category='error')
    if client.profile_picture:
        return render_template('client_profile.html', user=client, profile_picture=url_for('static', filename='profile_pictures/' + client.profile_picture))
    return render_template('client_profile.html', user=client)


@views.route('/my-plan', methods=['GET', 'POST'])
@login_required
def my_plan():
    return render_template("my_plan.html", user=current_user)

@views.route('/recipes', methods=['GET', 'POST'])
@login_required
def recipes():
    recipe_list = Recipe.query.all()
    return render_template("recipes.html", user=current_user, recipe_list=recipe_list)

@views.route('/progress', methods=['GET', 'POST'])
@login_required
def progress():
    return render_template("progress.html", user=current_user)

@views.route('/client-list', methods=['GET', 'POST'])
@login_required
def client_list():
    return render_template("client_list.html", user=current_user)

@views.route('/nutritionist-profile', methods=['GET', 'POST'])
@login_required
def nutritionist_profile():
    #recipe_list = []
    nutritionist = Nutritionist.query.get(current_user.id)

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

        elif request.method == 'POST':
            title = request.form.get('title')
            recipe_type = request.form.get('recipe_type')
            description = request.form.get('description')
    
            # Retrieve and validate ingredient fields
            ingredients = {}
            ingredient_counter = 1
            while f'ingredient-{ingredient_counter}' in request.form:
                ingredient_name = request.form.get(f'ingredient-{ingredient_counter}')
                amount = request.form.get(f'amount-{ingredient_counter}')

                # Check if ingredient already exists in the database
                existing_ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
                if existing_ingredient:
                    ingredients[existing_ingredient] = amount
                else:
                    new_ingredient = Ingredient(name=ingredient_name)
                    db.session.add(new_ingredient)
                    db.session.commit()
                    ingredients[new_ingredient] = amount
        
                ingredient_counter += 1
    
            new_recipe = Recipe(title=title, recipe_type=recipe_type,ingredients=ingredients, description=description)
    
            db.session.add(new_recipe)
            db.session.commit()
            flash('Recipe added!', category='success')
            return redirect(url_for('views.recipes'))

    #current_recipe = Recipe.query.filter_by(id=new_recipe.id).first()
    #recipe_list.append(current_recipe)

    if nutritionist.profile_picture:
        return render_template('nutritionist_profile.html', user=nutritionist, profile_picture=url_for('static', filename='profile_pictures/' + nutritionist.profile_picture))
    return render_template('nutritionist_profile.html', user=nutritionist)


@views.route('/accept_request', methods=['POST'])
def accept_request():
    client_id = request.form.get('client_id')
    nutritionist_id = request.form.get('nutritionist_id')

    client = Client.query.get(client_id)
    nutritionist = Nutritionist.query.get(nutritionist_id)

    if not client or not nutritionist:
        return '', 404

    client.nutritionist = nutritionist
    db.session.commit()

    return '', 200

@views.route('/reject_request', methods=['POST'])
def reject_request():
    client_id = request.form.get('client_id')
    nutritionist_id = request.form.get('nutritionist_id')

    client = Client.query.get(client_id)
    nutritionist = Nutritionist.query.get(nutritionist_id)

    if not client or not nutritionist:
        return '', 404

    client.nutritionist = None
    db.session.commit()

    return '', 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
