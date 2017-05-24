from Flask import Blueprint, request, render_template
from server import db
import models
from app.auth.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """Handles login actions """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

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
