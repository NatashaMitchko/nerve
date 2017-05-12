from jinja2 import StrictUndefined
import os, sys
from datetime import datetime

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session

from model import User, UserChallenge, Challenge, connect_to_db, db, example_data


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "81CAEB25176HDG36710KSXZ2320"

UPLOAD_FOLDER = '/static/images'
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


def get_user_id_by_username(name):
    """Takes username and returns user_id, else returns None

        >>> get_user_id_by_username('Shmlony')
        (1,)
        >>> get_user_id_by_username('not a person')
        None
    """
    user_id = db.session.query(User.id).filter(User.username==name).first()
    return user_id 

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


@app.route('/profile/<username>')
def load_user_profile(username):
    """Shows the profile of the specified User and their UserChallenges
    If the user clicks their own profile icon they will go to their profile, if
    they click another profile it will load that users profile and challenges.
    """
    user_id = get_user_id_by_username(username)
    info = get_profile_page_info(user_id)
    if user_id:
        return render_template('profile.html', 
                                username=username, 
                                info=info)
    else:
        flash("Not a valid user.")
        return redirect('/')

def check_password(user_id, password):
    """Checks to see if entered password matches the db password"""
    is_valid = db.session.query(User.password).filter(User.id==user_id).first()
    return (password == is_valid[0])

@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """Handles login actions """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # print username, password

        user_id = get_user_id_by_username(username)

        if user_id: # user exists
            if check_password(user_id, password):
                session['active'] = True
                session['user_id'] = user_id
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
        password = request.form.get('password')
        phone = request.form.get('tel')
        email = request.form.get('email')

        user_id = get_user_id_by_username(username) # None evaluates to False

        if user_id:
            flash('Username taken')
            return redirect('/register')
            # TODO: make this make sense:
        # elif is_session_active():
        #     return redirect('/logout')
        else:
            # Add new user to the database
            post_user(username, password, email, phone)
            # Add new user to the session
            user_id = get_user_id_by_username(username)
            session['active'] = True
            session['user_id'] = user_id
            flash('Welcome')
            return redirect('/')
    else:
        return render_template('register.html')

def allowed_file(filename):
    """Makes sure that the uploaded file is valid type"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def post_challenge(t, d, l, f):
    """Creates a new challenge and adds it to the db session"""
    new_challenge = Challenge(title=t, description=d, difficulty=l, file=f)
    db.session.add(new_challenge)
    db.session.commit()

@app.route('/create', methods=['GET', 'POST'])
def create_challenge():
    """Render new challenge form and post newly created challenges if valid"""
    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')
        difficulty = request.form.get('difficulty')
        file = request.files.get('file')

        if file.filename == '':
            flash('No file selected')
            return redirect('/create')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = '/static/images' + filename
            post_challenge(title, description, difficulty, filename)
            challenge = Challenge.query.filter_by(title==title)
            return redirect('/challenge/{}'.format(challenge.id))
    else:
        return render_template('create.html')

@app.route('/challenges')
def show_all_challenges():
    """Shows a list of all available challenges"""
    challenges = Challenge.query.order_by(Challenge.difficulty).all()
    return render_template('challenges.html', challenges=challenges)

@app.route('/challenge/<id>')
def challenge_details(id):
    challenge = Challenge.query.get(id)
    return render_template('challenge.html', challenge=challenge)

@app.route('/accept.json', methods=['POST'])
def accept_challenge():
    """Called whenever a user clicks 'accept' on a challenge.
    Also handles non-logged in users."""
    challenge_id = int(request.form.get('challenge_id'))
    user_id = int(session['user_id'])
    accepted_challenge = UserChallenge(user_id=user_id, 
                                        challenge_id=challenge_id, 
                                        accepted_timestamp=datetime.now())
    db.session.add(accepted_challenge)
    db.session.commit()

    return ''

if __name__ == "__main__":

    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app, 'postgres:///test_nerve') 

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    db.create_all()

    app.run(port=5000, host='0.0.0.0')