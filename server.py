from jinja2 import StrictUndefined
import os, sys
from datetime import datetime
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from werkzeug.utils import secure_filename
from model import User, UserChallenge, Challenge, ChallengeCategory, Category, connect_to_db, db, example_data
from vision import get_tags_for_image, image_is_safe
from flask.ext.bcrypt import Bcrypt
from sqlalchemy import exc
import arrow


app = Flask(__name__)
bcrypt = Bcrypt(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "81CAEB25176HDG36710KSXZ2320"

UPLOAD_FOLDER = 'static/images'
# To be compatible with cloudvision api:
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'raw', 'ico']) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Raise error for undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

def is_session_active():
    """Checks if a user is logged in or not, if there is no active key stored
    in the session one is created"""
    if session.has_key('active'):
        return session['active']
    session['active'] = False
    session['user_id'] = ''
    return session['active']

@app.route('/')
def index():
    """Homepage."""
    is_session_active()
    return render_template('/homepage.html')


def get_user_by_username(name):
    """Takes username and returns user object, else returns None
    """
    user = User.query.filter(User.username==name).first()
    return user

def get_user_by_id(user_id):
    """Takes user id and returns user object"""
    user = User.query.filter(User.id==user_id).first()
    return user

def get_profile_page_info(user_id):
    """Return relevant data to be displayed on profile page.

        >>> get_profile_page_info('Schmlandula')
        [(<UserChallenge challenge_id:2 id:6>, <Challenge title:Bring Down the Federation id:2>)]
        >>> get_profile_page_info('Shmlony')
        []
    """
    info = db.session.query(UserChallenge, 
            Challenge).join(Challenge).filter(UserChallenge.user_id==user_id)
    return info.all()

@app.route('/profile/id/<user_id>')
def to_profile_from_id(user_id):
    """Redirect to user profile through user id"""
    user = get_user_by_id(user_id)
    if user:
        return redirect('/profile/{}'.format(user.username))
    flash("Not a valid user.")
    return redirect('/')


@app.route('/profile/<username>')
def load_user_profile(username):
    """Shows the profile of the specified User and their UserChallenges
    If the user clicks their own profile icon they will go to their profile, if
    they click another profile it will load that users profile and challenges.
    """
    user = get_user_by_username(username)
    if user:
        info = get_profile_page_info(user.id)
        return render_template('profile.html', 
                                username=username, 
                                info=info)
    else:
        flash("Not a valid user.")
        return redirect('/')

@app.route('/time.json')
def humanize_timestamp():
    datetime_time = request.args.get('ISO_string')
    arrow_time_object = arrow.get(datetime_time)
    return arrow_time_object.humanize()

def check_password(db_password, password):
    """Checks to see if entered password matches the db password"""
    return bcrypt.check_password_hash(db_password, password)

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """Handles login actions """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # print username, password

        user = get_user_by_username(username)

        if user: # user exists
            if check_password(user.password, password):
                session['active'] = True
                session['user_id'] = user.id
                return redirect('/')
            else:
                flash('Incorrect password')
                return redirect('/login')
        else:
            flash('Incorrect Username')
            return redirect('/login')
    else:
        return render_template('/login.html', username='')

@app.route('/logout')
def logout():
    """Logged out users are redirected to the homepage"""
    session.clear()
    return redirect('/')

def post_user(u,p,e,f):
    """Creates new user and adds user to the db session"""
    new_user = User(username=u, password=p, email=e, phone=f)
    db.session.add(new_user)
    db.session.commit()

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Render new user signup form and handles new user post requests"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = bcrypt.generate_password_hash(request.form.get('password'))
        phone = request.form.get('tel')
        email = request.form.get('email')

        user = get_user_by_username(username) # None evaluates to False

        if user:
            flash('Username taken')
            return redirect('/register')
            # TODO: make this make sense:

        else:
            # Add new user to the database
            post_user(username, password, email, phone)
            # Add newly created user to the session
            session['active'] = True
            session['user_id'] = User.query.filter(username==username).first().id
            flash('Welcome')
            return redirect('/')
    else:
        return render_template('register.html')

def allowed_file(filename):
    """Makes sure that the uploaded file is valid type"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def post_challenge(t, d, l, f):
    """Creates a new challenge and adds it to the db"""
    new_challenge = Challenge(title=t, description=d, difficulty=l, image_path=f)
    db.session.add(new_challenge)
    db.session.commit()

def post_categories(tag):
    """Adds new categories to db that are unique."""
    new_category = Category(tag=tag)
    db.session.add(new_category)
    print 'post categories'
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        print "{} already exists.".format(tag)

def post_challenge_categories(tag_list, challenge_id):
    """Adds records describing relations between an individual challenge and 
                multiple categories. If the category doesn't exist in the db it
                gets added and the relation is created."""
    i = 0
    while i < len(tag_list):
        category = db.session.query(Category).filter(Category.tag==tag_list[i]).first()
        print category
        if category:
            new_challenge_category = ChallengeCategory(category_id=category.id, 
                                                        challenge_id=challenge_id)
            db.session.add(new_challenge_category)
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                print "Relation between {tag} and challenge {id} already exists.".format(tag=tag_list[i], id=challenge_id)
            i = i + 1
            print i
        else:
            post_categories(tag_list[i])
            print 'else'

@app.route('/create', methods=['GET', 'POST'])
def create_challenge():
    """Render new challenge form and post newly created challenges if valid"""
    if request.method == 'POST':

        title = request.form.get('title').title()
        description = request.form.get('description')
        difficulty = request.form.get('difficulty')
        file = request.files['file']

        if file.filename == '':
            flash('No file selected')
            return redirect('/create')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = 'static/images/' + filename
            if image_is_safe(filename):
                tag_list = get_tags_for_image(filename, 10)
                if tag_list:
                    post_challenge(title, description, difficulty, filename)
                    challenge_id = db.session.query(Challenge.id).filter(Challenge.title==title).first()
                    post_challenge_categories(tag_list, challenge_id[0])
                    return redirect('/challenge/{}'.format(challenge_id[0]))
                else:
                    flash("""We weren't able to analyze your image. Please 
                        choose another and try again""")
                    return redirect('/create')
    else:
        return render_template('create.html')

@app.route('/challenges')
def show_all_challenges():
    """Shows a list of all available challenges"""
    challenges = Challenge.query.order_by(Challenge.difficulty).all()
    return render_template('challenges.html', challenges=challenges)

@app.route('/challenge/<id>')
def challenge_details(id):

    challenge = db.session.query(Challenge, ChallengeCategory).filter(Challenge.id==id).join(ChallengeCategory).all()
    return render_template('challenge.html', challenge=challenge)

@app.route('/accept.json', methods=['POST'])
def accept_challenge():
    """Called whenever a user clicks 'accept' on a challenge."""
    challenge_id = int(request.form.get('challenge_id'))
    user_id = int(session['user_id'])
    accepted_challenge = UserChallenge(user_id=user_id, 
                                        challenge_id=challenge_id, 
                                        accepted_timestamp=datetime.now())
    db.session.add(accepted_challenge)
    db.session.commit()

    accepted_challenge = UserChallenge.query.filter(user_id==user_id, challenge_id==challenge_id)
    return str(accepted_challenge.first().id)

@app.route('/remove.json', methods=['POST'])
def remove_challenge():
    """Called whenever a user clicks 'remove' on a challenge."""
    challenge_id = int(request.form.get('challenge_id'))
    user_id = int(session['user_id'])

    # return the UC primary key

    return ''

def calculate_score(hits, difficulty):
    """Calculates the score for a winning image"""
    score = (10 * difficulty * hits)
    return score

def attempt_challenge(id, hits):
    """Updates the UserChallenge record with additional details"""
    user =  session['user_id']
    update = UserChallenge.query.filter((UserChallenge.user_id==session['user_id'])&(UserChallenge.challenge_id==id)).first()
    difficulty = Challenge.query.get(id).difficulty
    if hits:
        score = calculate_score(hits, difficulty)
        update.points_earned = score
        update.is_completed = True
        update.completed_timestamp = datetime.now()
    update.attempts += 1
    db.session.commit()

def image_match(tag_list, winning_tags):
    """Checks uploaded image tags against the challenge image"""
    hits = 0
    for tag in tag_list:
        if tag in winning_tags:
            hits += 1
    return hits

@app.route('/complete/<id>', methods=['GET','POST'])
def complete_challenge(id):
    """Gets UserChallenge page for uncompleted challenge and allows user
        to complete"""
    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            flash('No file selected')
            return redirect('/complete/{}'.format(id))
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = 'static/images/' + filename
            if image_is_safe(filename):
                tag_list = get_tags_for_image(filename, 5)
                categories = ChallengeCategory.query.filter(ChallengeCategory.challenge_id==id).all()
                winning_tags = [i.category.tag for i in categories]
                hits = image_match(tag_list, winning_tags)
                attempt_challenge(id, hits)
                return redirect('/complete/{}'.format(id))
            else:
                os.remove(filename)

    else:
        to_complete = db.session.query(UserChallenge, Challenge).filter(UserChallenge.id==id).join(Challenge).first()
        return render_template('complete.html', challenge_info=to_complete)

@app.route('/contact-me')
def contact_me():
    """My profile page that shows how to get in contact with me"""
    return render_template('contact_me.html')




if __name__ == "__main__":

    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app, 'postgres:///test_nerve')

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    db.create_all()

    app.run(port=5000, host='0.0.0.0')