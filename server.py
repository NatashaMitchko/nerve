from jinja2 import StrictUndefined
import os, sys
from datetime import datetime
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from werkzeug.utils import secure_filename
from model import User, UserChallenge, Challenge, ChallengeCategory, Category, UserChallengeCategory, connect_to_db, db, example_data
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
    """Takes ISO string passed from challenge object and converts it to
    a humanized timestamp"""
    datetime_time = request.args.get('ISO_string')
    arrow_time_object = arrow.get(datetime_time)
    return arrow_time_object.humanize()

@app.route('/num-players.json')
def num_players():
    """Counts how many users are participating in each challenge"""
    challenge_id = request.args.get('challenge_id')
    query = UserChallenge.query.filter(UserChallenge.challenge_id==challenge_id)
    print query.count()
    return str(query.count())

def check_password(db_password, password):
    """Checks to see if entered password matches the db password"""
    return bcrypt.check_password_hash(db_password, password)

@app.route('/login')
def show_entry_forms():
    """Render login/register form"""
    return render_template('login-register.html')

@app.route('/username_taken.json')
def is_username_taken():
    """Checks if username exists in Users table, returns T/F"""
    username = request.args.get('username')
    print username
    user = get_user_by_username(username)
    print bool(user)
    is_user = {'username-taken': bool(user)}
    return jsonify(is_user)

@app.route('/login', methods=['POST'])
def show_login_form():
    """Handles login attempts"""
    username = request.form.get('username')
    password = request.form.get('password')
    # print username, password

    user = get_user_by_username(username)

    if user: # user exists
        if check_password(user.password, password):
            session['active'] = True
            session['user_id'] = user.id
            return redirect('/challenges')
        else:
            flash('Incorrect password')
            return redirect('/login')
    else:
        flash('Incorrect Username')
        return redirect('/login')

@app.route('/logout')
def logout():
    """Logged out users are redirected to the homepage"""
    session['active'] = False
    session['user_id'] = ''
    return redirect('/login')

def post_user(u,p,e,f):
    """Creates new user and adds user to the db session"""
    new_user = User(username=u, password=p, email=e, phone=f)
    db.session.add(new_user)
    db.session.commit()

@app.route('/register', methods=['POST'])
def register_user():
    """Handles user creation requests"""

    username = request.form.get('username')
    password = bcrypt.generate_password_hash(request.form.get('password'))
    phone = request.form.get('tel')
    email = request.form.get('email')

    user = get_user_by_username(username) # None evaluates to False

    if user:
        flash('Username taken')
        return redirect('/register')
    else:
        post_user(username, password, email, phone)
        # Add newly created user to the session
        session['active'] = True
        session['user_id'] = User.query.filter(username==username).first().id
        return redirect('/challenges')

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
    print 'posted', tag
    try:
        db.session.commit()
        return new_category
    except exc.IntegrityError:
        db.session.rollback()
        print "{} already exists in the Category table.".format(tag)

def post_challenge_categories(tag_set, challenge_id):
    """Adds records describing relations between an individual challenge and 
                multiple categories. If the category doesn't exist in the db it
                gets added and the relation is created. Does not create 
                duplicate records in ChallengeCategory table either. """
  
    for tag in tag_set:
        category = db.session.query(Category).filter(Category.tag==tag).first()
        if category:
            print category, 'is in the Categories table and is ready to be added as a ChallengeCategory'
            new_challenge_category = ChallengeCategory(category_id=category.id, 
                                                        challenge_id=challenge_id)
            db.session.add(new_challenge_category)
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                print "Relation between {tag} and challenge {id} already exists.".format(tag=tag, id=challenge_id)
        else:
            print tag, 'was not in the Categories table and needs to be added'
            # commits new category
            category = post_categories(tag)
            # new transaction
            new_challenge_category = ChallengeCategory(category_id=category.id, 
                                                        challenge_id=challenge_id)
            db.session.add(new_challenge_category)
            # Following try/except block catches exceptions that may arise from
            # the category&challenge unique constraint via the composite index
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                print "Relation between {tag} and challenge {id} already exists.".format(tag=tag, id=challenge_id)


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
            return redirect('/challenges')
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
                    return redirect('/challenges')

@app.route('/challenges')
def show_all_challenges():
    """Shows a list of all available challenges"""
    if session['active']:
        user = get_user_by_id(session['user_id'])
        username = user.username
    else:
        username = ''
    challenges = Challenge.query.order_by(Challenge.difficulty).all()
    return render_template('challenges.html', challenges=challenges, username=username)

@app.route('/is_completed.json')
def is_challenge_completed():
    """Returns accepted or copmleted (not accepted is default - empty string 
        returned to JS) for each challenge on the page 
    depending on the state of the challenge in the context of the requesting user""" 
    if is_session_active():
        challenge_id = request.args.get('challenge_id')
        user_id = session['user_id']
        query = db.session.query(UserChallenge.is_completed).filter(UserChallenge.challenge_id==challenge_id)
        result = query.filter(UserChallenge.user_id==user_id).first()
        # result is a tuple OR none - ugh
        # 'NoneType' object has no attribute '__getitem__'
        if not result:
            return ''
        elif result[0]:
            return jsonify({'status': 'completed'})
        elif not result[0]:
            return jsonify({'status': 'accepted'})
    else:
        return ''

def leaderboard(challenge_id):
    """Given a challenge id return list of tuples ordered by highest score that
        contain username and score"""
    query = UserChallenge.query.filter((UserChallenge.challenge_id==challenge_id)&(UserChallenge.is_completed==True)).order_by(UserChallenge.points_earned)
    winners_list = query.limit(6).all()
    print "hello ", winners_list
    return winners_list

@app.route('/challenge/<id>')
def challenge_details(id):
    """Renders that challenge details and analytics page"""
    username = get_user_by_id(session['user_id']).username
    challenge = db.session.query(Challenge, ChallengeCategory).filter(Challenge.id==id).join(ChallengeCategory).all()
    winners = leaderboard(id)
    print winners, "route print"
    return render_template('challenge.html', challenge=challenge, username=username, winners=winners)

@app.route('/completion-stats.json')
def get_completion_stats():
    """Generates a dictionary of data to be used by chart.js on challenge analytics
        page"""
    challenge_id = request.args.get('challenge_id')
    query = UserChallenge.query.filter(UserChallenge.challenge_id==challenge_id)
    finished = query.filter(UserChallenge.is_completed==True).count()
    unfinished = query.filter(UserChallenge.is_completed==False).count()

    data = {'finished':int(finished), 'unfinished':int(unfinished)}
    print data
    return jsonify(data)

@app.route('/accept.json', methods=['POST'])
def accept_challenge():
    """Called whenever a user clicks 'accept' on a challenge."""
    challenge_id = int(request.form.get('challenge_id'))
    user_id = int(session['user_id'])
    accepted_challenge = UserChallenge(user_id=user_id, 
                                        challenge_id=challenge_id, 
                                        accepted_timestamp=datetime.now())
    db.session.add(accepted_challenge)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        print 'User has already accepted this challenge.'
        return ''

    accepted_challenge = UserChallenge.query.filter(user_id==user_id, challenge_id==challenge_id)
    return str(accepted_challenge.first().id)

@app.route('/remove.json', methods=['POST'])
def remove_challenge():
    """Called whenever a user clicks 'remove' on a challenge."""
    challenge_id = int(request.form.get('challenge_id'))
    user_id = int(session['user_id'])

    # return the UC primary key

    return ''

def calculate_score(hits, difficulty, attempts):
    """Calculates the score for a winning image
    attempts +1 because this is called before attempt increment comitted to db"""
    score = (10 * difficulty/(attempts+1))*len(hits)
    return score

def attempt_challenge(id, hits, filename):
    """Updates the UserChallenge record with details of attempt 
    returns UserChallenge object"""

    user =  session['user_id']
    update = UserChallenge.query.filter((UserChallenge.user_id==session['user_id'])&(UserChallenge.challenge_id==id)).first()
    difficulty = Challenge.query.get(id).difficulty

    # empty set is false
    if hits:
        score = calculate_score(hits, difficulty, update.attempts)
        update.points_earned = score
        update.is_completed = True
        update.image_path = filename
        print filename +  ':filename'
        update.completed_timestamp = datetime.now()
    update.attempts += 1
    db.session.commit()
    return update

def save_winning_hits(tag_set, user_challenge_id):
    """Adds information relating UserChallenge to Category"""
    for tag in tag_set:
        # Get category id for hit
        category = Category.query.filter(Category.tag==tag).first()
        new_user_challenge_category = UserChallengeCategory(user_challenge_id=user_challenge_id,
                                                            category_id=category.id)
        db.session.add(new_user_challenge_category)
        db.session.commit()

@app.route('/complete/<id>', methods=['POST'])
def complete_challenge(id):
    """Gets UserChallenge page for uncompleted challenge and allows user
        to complete"""
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect('/complete/{}'.format(id))
    elif file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filename = 'static/images/' + filename

        if image_is_safe(filename):
            tag_set = get_tags_for_image(filename, 5)
            categories = ChallengeCategory.query.filter(ChallengeCategory.challenge_id==id).all()
            winning_tags = {i.category.tag for i in categories}
            
            hits = winning_tags.intersection(tag_set)

            user_challenge = attempt_challenge(id, hits, filename)

            if len(hits) != 0:
                save_winning_hits(tag_set, user_challenge.id)
            return redirect('/complete/{}'.format(id))
        else:
            os.remove(filename)
            flash('Try another image')
            return redirect('/complete/{}'.format(id))

@app.route('/matched_attributes.json')
def matched_attributes():
    """Using challenge id and user_id from the session, get all attributes that
    matched for that user to complete the challenge"""
    user_challenge_id = request.args.get('user_challenge_id')
    categories = UserChallengeCategory.query.filter(UserChallengeCategory.user_challenge_id==user_challenge_id).all()
    winning_tags_to_display = {i.category.tag for i in categories}
    dict = {}
    for tag in winning_tags_to_display:
        dict.setdefault(tag, 0)
    return jsonify(dict)

@app.route('/challenge_attributes.json')
def challenge_attributes():
    """Returns a dict of all challenge attributes for analytics page"""
    challenge_id = request.args.get('challenge_id')
    print challenge_id
    categories = ChallengeCategory.query.filter(ChallengeCategory.challenge_id==challenge_id).all()
    tags_to_display = [i.category.tag for i in categories]
    print tags_to_display
    dict = {}
    for tag in tags_to_display:
        dict.setdefault(tag, 0)
    print dict
    return jsonify(dict)

def make_d3_nodes():
    """Create individual dictionaries for each challenge
        >>> make_d3_nodes()
        [{u'Bridge': 1}, {u'Bird': 2}]
    """
    # get all challenge objects
    challenges = Challenge.query.all()
    # make the challenge nodes
    nodes_list = []
    i = 0
    for challenge in challenges:
        node = {"id": challenge.title, "group": i+1}
        # node.setdefault(challenge.title, i+1)
        nodes_list.append(node)
        i += 1
    return nodes_list

def make_d3_links():
    """create the individual dictionaries for each link betweek categories

    """
    # get all challenge categories in order of challenge id
    challege_categories = db.session.query(ChallengeCategory).order_by(ChallengeCategory.category_id).all()
    links_list = []
    for i in range(len(challege_categories) - 1):
        if challege_categories[i].category_id == challege_categories[i + 1].category_id:
            link = {"source": challege_categories[i].challenge.title,
                    "target": challege_categories[i + 1].challenge.title,
                    "value": challege_categories[i].category.tag
                    }
            links_list.append(link)
        i += 1
    return links_list

@app.route('/challenge_analytics.json')
def challenge_analytics():
    """Returns information to resolve D3 diagram that shows the relationship
                between challenges by keywords they have in common"""
    node_values = make_d3_nodes()
    link_values = make_d3_links()

    d3_dict = {"nodes": node_values, "links": link_values}

    print d3_dict

    return jsonify(d3_dict)

@app.route('/contact-me')
def contact_me():
    """My profile page that shows how to get in contact with me"""
    return render_template('contact_me.html')


if __name__ == "__main__":

    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app, 'postgres:///nerve')
    db.create_all()

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug


    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')