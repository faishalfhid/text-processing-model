import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form', response.data)

    def test_index_post(self):
        response = self.app.post('/', data={'message': 'Ini pesan spam'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="prediction-nb"', response.data)
        self.assertIn(b'id="prediction-svm"', response.data)

if __name__ == '__main__':
    unittest.main()