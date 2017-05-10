from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session

from model import User, UserChallenge, Challenge, connect_to_db, db, example_data

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "81CAEB25176HDG36710KSXZ2320"


# Raise error for undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""

    return render_template('/homepage.html')

def get_user_id_by_username(name):
    """Takes username and returns user_id, else returns False

        >>> get_user_id_by_username('Shmlony')
        (1,)
        >>> get_user_id_by_username('not a person')
        False

    """
    try:
        user_id = db.session.query(User.id).filter(User.username==name).one()
        return user_id 
    except:
        return False

def get_profile_page_info(name):
    """Return relevant data to be displayed on profile page.

        >>> get_profile_page_info('Schmlandula')
        [(<UserChallenge challenge_id:2 id:6>, <Challenge title:Bring Down the Federation id:2>)]
        >>> get_profile_page_info('Shmlony')
        []

    """

    user_id = get_user_id_by_username(name)

    if user_id:
        info = db.session.query(UserChallenge, Challenge).join(Challenge).filter(UserChallenge.user_id==user_id)
        return info.all()
    else:
        return False

@app.route('/profile/<username>')
def load_user_profile(username):
    """Shows the profile of the specified User and their UserChallenges
    If the user clicks their own profile icon they will go to their profile, if
    they click another profile it will load that users profile and challenges.
    """

    info = get_profile_page_info(username)
    if info:
        return render_template('profile.html', 
                                username=username, 
                                info=info)
    else:
        flash("Not a valid user.")
        return redirect('/')

def check_password(user_id, password):
    """Checks to see if entered password matches the db password"""
    is_valid = db.session.query(User.password).filter(User.id==user_id)
    return (password == is_valid)


@app.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """Handles login actions """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print username, password

        user_id = get_user_id_by_username(username)

        if user_id: # user exists
            if check_password(user_id, password):
                session['user_id'] = user_id[0] # Add id number to session
                return redirect('/')
            else:
                flash('Incorrect password')
                return redirect('/login')
        else:
            flash('Incorrect Username')
            return redirect('/login')
    else:
        return render_template('/login_form.html', username='')

@app.route('/logout')
def logout():
    """Logged out users are redirected to the homepage"""
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Render new user signup form and post data"""
    if request.method == 'POST':
        
    else:
        return render_template('register.html')



if __name__ == "__main__":

    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app, 'postgres:///test_nerve') 

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    db.create_all()

    app.run(port=5000, host='0.0.0.0')