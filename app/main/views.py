from flask import render_template,request,redirect,url_for,abort
from . import main
from ..requests import get_recipes,get_recipe,search_recipe
from .forms import ReviewForm,UpdateProfile
from ..models import Review,User,PhotoProfile
from flask_login import login_required, current_user
from .. import db,photos
import markdown2  

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting popular movie
    # popular_movies = get_movies('popular')
    # upcoming_movie = get_movies('upcoming')
    # now_showing_movie = get_movies('now_playing')
    recipes = get_recipes()
    print(recipes)


    title = 'Home - Welcome to The best Movie Review Website Online'

    search_recipe = request.args.get('recipe_query')

    if search_recipe:
        return redirect(url_for('.search',recipe_name=search_recipe))
    else:
        return render_template('index.html', title = title, recipes = recipes)


@main.route('/recipe/<int:id>')
def recipe(id):

    '''
    View recipe page function that returns the recipe details page and its data
    '''
    recipe = get_recipe(id)
    title = f'{recipe.title}'
    reviews = Review.get_reviews(recipe.id)

    return render_template('recipe.html',title = title,recipe = recipe,reviews = reviews)



@main.route('/search/<recipe_name>')
def search(recipe_name):
    '''
    View function to display the search results
    '''
    recipe_name_list = recipe_name.split(" ")
    recipe_name_format = "+".join(recipe_name_list)
    searched_recipes = search_recipe(recipe_name_format)
    title = f'search results for {recipe_name}'
    return render_template('search.html',recipes = searched_recipes)


@main.route('/recipe/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):

    form = ReviewForm()

    recipe = get_recipe(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data

        # Updated review instance
        new_review = Review(recipe_id=recipe.id,recipe_title=title,image_path=recipe.poster,recipe_review=review,user=current_user)

        # save review method
        new_review.save_review()
        return redirect(url_for('.recipe',id = recipe.id ))

    title = f'{recipe.title} review'
    return render_template('new_review.html',title = title, review_form=form, recipe=recipe)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/review/<int:id>')
def single_review(id):
    review=Review.query.get(id)
    if review is None:
        abort(404)
    format_review = markdown2.markdown(review.recipe_review,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('review.html',review = review,format_review=format_review)    