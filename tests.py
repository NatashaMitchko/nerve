import unittest
import sys, os

# uncomment below when ready to test server
from server import app 

from model import User, UserChallenge, Challenge, db, example_data, connect_to_db, init_app
from server import get_user_id_by_username, get_profile_page_info

class NerveTestsServerHelperFunctinos(unittest.TestCase):
    """Make sure the helper functions in the server work"""

    def setUp(self):
        """Set testing to true, import functions from server"""
        
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, 'postgresql:///test_nerve')
        db.create_all()
        example_data()

    def tearDown(self):
        """Runs at the end of every test."""

        db.session.close()
        db.drop_all()

    def test_get_user_id_by_username(self):
        """should return none for non-users, get user_id for users"""
        not_a_uer = get_user_id_by_username('Jeffry')
        self.assertFalse(not_a_uer, 'Result was of type that did not evaluate to False (not expected user was in db)')
        a_user = get_user_id_by_username('Shmlony')
        self.assertTrue(a_user, 'Result was of type that did not evaluate to True (expected user was not in db)')

class NerveTestsRegistration(unittest.TestCase):
    """Do post requests to create new users/ accept challenges/ create new challenges
    sucessfully create records in the db"""

    def setUp(self):
        """Runs before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # test_nerve is the name of the test database
        # connect_to_db comes from model.py

        connect_to_db(app, 'postgresql:///test_nerve')

        # Create tables and adds sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Runs at the end of every test."""

        db.session.close()
        db.drop_all()

    def test_create_user(self):
        """Is registration sucessful
        - redirect home
        - add record to users table"""
        result = self.client.post('/register',
                                  data={'username': 'Jane',
                                        'password': 'password',
                                        'email': 'jane@jane.com',
                                        'phone': '123-456-7890'},
                                  follow_redirects=True)
        self.assertNotIn('Log In', result.data)
        self.assertIn('Welcome', result.data)
        self.assertIn('Log Out', result.data)
        new_user_obj = db.session.query(User).filter(User.username=='Jane').one() # Example data from setup has no Janes
        self.assertEqual(new_user_obj.email, 
                        'jane@jane.com', 
                        'User record was not sucessfully created')

    def test_create_challenge(self):
        """Does a post request to create a challenge add a record to that table"""
        result = self.client.post('/create',
                                  data={'title': 'Cinnamon Challenge',
                                        'description': 'Eat a whole spoonful of cinnamon',
                                        'difficulty': '3',
                                        'file': '/static/image/cinnamon.png'},
                                  follow_redirects=True)
        self.assertNotIn('Title', result.data, 'Challenge detail page did not load, still on input form page.')
        self.assertNotIn('Welcome', result.data, 'Challenge detail page did not load, redirected to homepage.')
        self.assertIn('Find a Challenge', result.data, 'User not presented with option to navigate to challenge list.')
        self.assertIn('<img src="/static/image/cinnamon.png"', result.data, 'Image tag did not populate with correct source.')
        new_challenge_obj = db.session.query(Challenge).filter(Challenge.title=='Cinnamon').one() # Example data from setup has no Cinnamon
        self.assertEqual(new_challenge_obj.description, 
                        'Eat a whole spoonful of cinnamon', 
                        'Challenge record was not sucessfully created')

    def test_accept_challenge(self):
        """Does accepting a challenge add the correct record to UserChallenge"""
        pass


class NerveTestsDatabaseQueries(unittest.TestCase):
    """Tests that query the database
    TODO: test for pagination when user has many challenges"""

    def setUp(self):
        """Runs before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # test_nerve is the name of the test database
        # connect_to_db comes from model.py

        connect_to_db(app, 'postgresql:///test_nerve')

        # Create tables and adds sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Runs at the end of every test."""

        db.session.close()
        db.drop_all()

    def test_profile_page_no_challenges(self):
        """Does profile page for the user in session with no challenges 
        show options to create challenge and/or accept existing challenges"""
        with self.client as c:
            with c.session_transaction() as s:
                s['active'] = False
                s['user_id'] = ''
        result = self.client.get('/profile/Shmlony', follow_redirects=True) # see example_data() in model.py for test user attributes
        self.assertNotIn('Accepted', result.data)
        self.assertNotIn('Completed', result.data)
        self.assertIn('Create a Challenge', result.data)
        self.assertIn('Find a Challenge', result.data)

    def test_profile_page_one_in_progress(self):
        """Tests content for profile page where user in session has only 
        challenges that are in progress"""
        with self.client as c:
            with c.session_transaction() as s:
                s['active'] = False
                s['user_id'] = ''

        result = self.client.get('/profile/Shmlantha', follow_redirects=True) # see example_data() in model.py for test user attributes
        self.assertIn('Accepted', result.data)
        self.assertNotIn('Completed', result.data)
        self.assertIn('Create a Challenge', result.data) 
        self.assertIn('Find a Challenge', result.data) 

    def test_profile_page_all_complete(self):
        """Tests profile page content where user in session has no active 
        challenges but does have completed challenges. They should see their 
        past completed challenges as well as options to create/ accept 
        challenges"""
        with self.client as c:
            with c.session_transaction() as s:
                s['active'] = False
                s['user_id'] = ''

        result = self.client.get('/profile/Schmlonathan', follow_redirects=True) # see example_data() in model.py for test user attributes
        self.assertIn('Accepted', result.data)
        self.assertIn('Completed', result.data)
        self.assertIn('Create a Challenge', result.data)
        self.assertIn('Find a Challenge', result.data)

    def test_invalid_user_profile(self):
        """User attempted to access a user profile for a user that doesn't exist"""
        with self.client as c:
            with c.session_transaction() as s:
                s['active'] = False
                s['user_id'] = ''

        result = self.client.get('/profile/Henry', follow_redirects=True)
        self.assertNotIn('Henry', result.data, 'Name from URL appeared on page.')
        self.assertIn('Home', result.data, 'Page did not redirect home.')
        self.assertIn('Not a valid user.', result.data, 'Did not flash "Not a valid user."')

    def test_view_all_challenges_logged_out(self):
        """Does the challenges page show content for logged out users"""
        with self.client as c:
            with c.session_transaction() as s:
                s['active'] = False
                s['user_id'] = ''

        result = self.client.get('/challenges')
        self.assertIn('<table>', result.data, 'Tables were not generated to display data')
        self.assertIn('Log In', result.data, 'Logged out user not presented with option to log in.')
        self.assertIn('View', result.data, 'Logged out user not provided option to navigate to challenge details')
        self.assertNotIn('<a href="" data-challenge_id="{{ challenge.id }}" class="accept-btn">Accept</a>', result.data, 'Logged out user provided option to accept challenge from list')
        self.assertNotIn('Log Out', result.data, 'Logged out user presented with option to log out.')


    def test_view_all_challenges_logged_in(self):
            """Does the challenges page show content for logged in users"""
            with self.client as c:
                with c.session_transaction() as session:
                    session['active'] = True
                    session['user_id'] = 1

            result = self.client.get('/challenges')
            self.assertIn('<table>', result.data, 'Tables were not generated to display data')
            self.assertIn('Log Out', result.data, 'Logged in user not presented with option to log out.')        
            self.assertIn('Accept', result.data, 'Logged in user not provided option to accept challenge from list')
            self.assertIn('View', result.data, 'Logged in user not provided option to navigate to challenge details')        
            self.assertNotIn('Log In', result.data, 'Logged in user presented with option to log in.')

    def test_view_single_challenge(self):
        """Does the challenge details page show the correct results"""
        with self.client as c:
            with c.session_transaction() as s:
                s['active'] = False
                s['user_id'] = ''
                
        result = self.client.get('/challenge/1')
        self.assertIn('Find a Challenge', result.data, 'User not provided option to navigate back to challenge list')


class NerveTestsPageData(unittest.TestCase):
    """Determine if the correct page is showing in the specified route"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_logged_in_homepage(self):
        """ Loged in users should be brought to the homepage, else prompted
        to log in.
        """

        with self.client as c:
            with c.session_transaction() as s:
                s['active'] = True
                s['user_id'] = 1

        result = self.client.get('/')
        self.assertIn('Log Out', result.data, 'Logged in user was not presented with option to log out.')
        self.assertNotIn('Log In', result.data, 'Logged out user was not presented with option to log in.')

if __name__ == "__main__":
    # Turn debug off in server before testing (redirects)

    os.system('dropdb test_nerve')
    os.system('createdb test_nerve')
    unittest.main()





