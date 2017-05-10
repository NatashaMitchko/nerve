import unittest

# uncomment below when ready to test server
from server import app 

from model import User, UserChallenge, Challenge, db, example_data, connect_to_db, init_app

class NerveTestsServerHelperFunctinos(unittest.TestCase):
    """Make sure the helper functions in the server work"""

    def setUp(self):
        """Set testing to true, import functions from server"""
        from server import get_user_id_by_username, get_profile_page_info
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
        """should return false for non-users, get user_id for users"""
        not_a_uer = get_user_id_by_username('Jeffry')
        self.assertFalse(not_a_uer, 'Jeffry is not a user in the db')
        a_user = get_user_id_by_username('Shmlony')
        self.assertTrue(a_user, 'Result was a string (String==True)')
        self.assertEqual(a_user, (1), 'User was ID:1 in db')

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
        """Does successful registration:
        - redirect home
        - add record to users table"""
        pass

    def test_create_challenge(self):
        """Does a post request to create a challenge add a record to that table"""
        pass

    def test_accept_challenge(self):
        """Does accepting a challenge add the correct record to UserChallenge"""
        pass


class NerveTestsDatabaseQueries(unittest.TestCase):
    """Flask tests that use the database.
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

        result = self.client.get('/profile/Shmlony') # see example_data() in model.py for test user attributes
        self.assertNotIn('Accepted', result.data)
        self.assertNotIn('Completed', result.data)
        self.assertIn('Create a Challenge', result.data)
        self.assertIn('Accept a Challenge', result.data)

    def test_profile_page_one_in_progress(self):
        """Tests content for profile page where user in session has only 
        challenges that are in progress"""

        result = self.client.get('/profile/Shmlantha') # see example_data() in model.py for test user attributes
        self.assertIn('Accepted', result.data)
        self.assertNotIn('Completed', result.data)
        self.assertIn('Create a Challenge', result.data) 
        self.assertIn('Accept a Challenge', result.data) 

    def test_profile_page_all_complete(self):
        """Tests profile page content where user in session has no active 
        challenges but does have completed challenges. They should see their 
        past completed challenges as well as options to create/ accept 
        challenges"""

        result = self.client.get('/profile/Schmlonathan') # see example_data() in model.py for test user attributes
        self.assertIn('Accepted', result.data)
        self.assertIn('Completed', result.data)
        self.assertIn('Create a Challenge', result.data)
        self.assertIn('Accept a Challenge', result.data)

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

        result = self.client.get('/')
        self.assertIn('Log Out', result.data)
        self.assertNotIn('Log In', result.data)



if __name__ == "__main__":
    # init_app()
    unittest.main()
