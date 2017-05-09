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

def get_profile_page_info(name):
    """Return relevant data to be displayed on profile page."""

    #fails for usernames that are not unique - added db constraint
    user_id = db.session.query(User.id).filter(User.username==name).one() 

    info = db.session.query(UserChallenge, Challenge).join(Challenge).filter(UserChallenge.user_id==user_id)
    return info.all()


@app.route('/profile/<username>')
def load_user_profile(username):
    """Shows the profile of the specified User and their UserChallenges
    If the user clicks their own profile icon they will go to their profile, if
    they click another profile it will load that users profile and challenges.
    """

    info = get_profile_page_info(username)
    return render_template('profile.html', 
                            username=username, 
                            info=info)

if __name__ == "__main__":

    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app, 'postgres:///test_nerve') 

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    db.create_all()

    app.run(port=5000, host='0.0.0.0')