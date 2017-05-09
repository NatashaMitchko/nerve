import unittest

from server import app
from model import User, UserChallenge, Challenge, db, example_data, connect_to_db

class NerveTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Runs before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # test_nerve is the name of the test database
        # connect_to_db comes from model.py
        connect_to_db(app, "postgresql:///test_nerve")

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
        pass

    def test_profile_page_one_in_progress(self):
        """Tests content for profile page where user in session has only 
        challenges that are in progress"""
        pass

    def test_profile_page_all_complete(self):
        """Tests profile page content where user in session has no active 
        challenges but does have completed challenges. They should see their 
        past completed challenges as well as options to create/ accept 
        challenges"""
        pass


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
                s['TODO:Session key for logged in'] = True

        result = self.client.get('/')
        self.assertIn('Log Out', result.data)
        self.assertNotIn('Log In', result.data)



if __name__ == "__main__":
    unittest.main()
