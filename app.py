import requests
import os
from datetime import date

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import SignUpForm, LoginForm, UserFoodForm
from models import db, connect_db, User, Ingredient, Like, Favorite, Recipe
from secrets import API_KEY, SECRET_KEY


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///ingredients')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)

# debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if "current_user" in session:
        g.user = User.query.get(session["current_user"])

    else:
        g.user = None

@app.route('/')
def home():
    """Home page"""
   
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """User Sign up form."""

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data, password=form.password.data, email=form.email.data)
            db.session.commit()
            
        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        session["current_user"] = user.id

        return redirect('/user')
    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Login user"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)
        if user:
            session["current_user"] = user.id

            return redirect('/user')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Logout User"""

    if "current_user" in session:
        del session["current_user"]
    
    return redirect('/')

@app.route('/user', methods=["GET", "POST"])
def user_food():
    """User ingredients/food page"""

    form = UserFoodForm()
    
    user_id = session["current_user"]
    user = User.query.get(user_id)
    food = user.ingredients
    today = date.today()

    if form.validate_on_submit():
        
        ingredient = form.ingredient.data
        description = form.description.data
        # categories = form.category.data
        quantity = form.quantity.data
        image = form.image.data
        purchase_date = form.purchase_date.data
        expiration_date = form.expiration_date.data
        alarm_date = form.alarm_date.data

        food = Ingredient(
            ingredient=ingredient,
            user_id=user_id,
            description=description,
            # categories=categories,
            quantity=quantity,
            image=image,
            purchase_date=purchase_date,
            expiration_date=expiration_date,
            alarm_date=alarm_date)
            
        db.session.add(food)
        db.session.commit()
        return redirect('/user')
    else:
        return render_template('food.html', form=form, food=food, date=today)


@app.route('/user/ingredient/<int:ingredient_id>/update', methods=['GET','POST'])
def edit_ingredient(ingredient_id):
    """Edit selected ingredient"""

    form = UserFoodForm()
    get_ingredient = Ingredient.query.get_or_404(ingredient_id)

    if form.validate_on_submit():
      
        ingredient = form.ingredient.data
        description = form.description.data
        # categories = form.category.data
        quantity = form.quantity.data
        image = form.image.data
        purchase_date = form.purchase_date.data
        expiration_date = form.expiration_date.data
        alarm_date = form.alarm_date.data

        get_ingredient.ingredient = ingredient
        get_ingredient.description = description
        # get_ingredient.categories = categories
        get_ingredient.quantity = quantity
        get_ingredient.image = image
        get_ingredient.purchase_date = purchase_date
        get_ingredient.expiration_date = expiration_date
        get_ingredient.alarm_date = alarm_date

        db.session.commit()
        return redirect('/user')
    else:
        return render_template("/user/ingredient.html", form=form, ingredient=get_ingredient)

@app.route('/user/ingredient/<int:ingredient_id>/delete', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    """Delete selected ingredient"""

    ingredient = Ingredient.query.get_or_404(ingredient_id)

    db.session.delete(ingredient)
    db.session.commit()
    
    return jsonify(message='Deleted')


@app.route('/user/recipe', methods=["GET","POST"])
def recipe():
    """Recipe of selected ingredients"""
    
    get_ingredient = request.form.getlist('ingredient')
    page = request.form['pages']
    if get_ingredient ==[]:
        
        flash('Please select ingredients', 'danger')
        return redirect('/user')
    else:
        ingredient = str(get_ingredient)[1:-1]
        recipe = requests.get('https://api.spoonacular.com/recipes/findByIngredients', params={'apiKey': API_KEY, 'ingredients':ingredient, 'number': page})
        list_recipe = recipe.json()
        return render_template('/user/recipe.html', list_recipe=list_recipe)

@app.route('/user/recipe/<int:recipe_id>/instructions', methods=["GET", "POST"])
def recipe_instructions(recipe_id):
    """Recipe Instruction"""

    instruct = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions', params={'apiKey': API_KEY})
    recipe_instruction = instruct.json()

    
    return render_template('/recipe/instructions.html', recipe_instruction=recipe_instruction)

# # modify below
@app.route('/user/recipe/favorites', methods=["GET", "POST"])
def favorites_recipes():
    """User Favorites Recipes"""

    user_id = g.user.id
    favorites = Favorite.query.get(user_id)
    if (favorites == None):
        favorites = []
        return render_template('/user/favorites.html', favorites=favorites) 
    else:
        return render_template('/user/favorites.html', favorites=favorites) 
    # favorites = ['hi', 'hola']

    # return render_template('/user/favorites.html', favorites=favorites) 

@app.route('/user/recipe/<int:recipe_id>/favorites', methods=["GET", "POST"])
def update_favorites_recipes(recipe_id):
    """User Favorites Recipes"""

    user_id = g.user.id
    favorites = Favorite(user_id=user_id, recipe_id=recipe_id)
    db.session.add(favorites)
    db.session.commit()
    # Recipe(user_id=user_id, recipe_id=recipe_id)
    # recipe = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/information', params={'apiKey': API_KEY})
    # favorites = recipe.json()

    # add redirect instead of return()
    # return redirect
    return render_template('/user/favorites.html', favorites=favorites)