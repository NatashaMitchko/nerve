from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session

import model import User as U, UserChallenge as UC, Challenge as C, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "81CAEB25176HDG36710KSXZ2320"

# Raise error for undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

