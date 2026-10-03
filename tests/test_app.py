import unittest
from app import app, db, Item

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_item(self):
        response = self.app.post('/create', data=dict(titulo='Test Item', descricao='This is a test item'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            item = Item.query.filter_by(titulo='Test Item').first()
            self.assertIsNotNone(item)

if __name__ == '__main__':
    unittest.main()
