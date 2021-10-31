from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class IntegrationTests(TestCase):
    def test_root_url(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<title>Boggle</title>", html) 
    def test_submit_guess(self):
        with app.test_client() as client:
            res = client.post('/submit-guess', json={
                'guess': 'word'
            })
            data = json.loads(res.get_data(as_text=True))
            self.assertEqual(res.status_code, 200)
            self.assertIn(data['Result'], {'not-on-board','not-a-word','ok'}) 
    def test_submit_score(self):
        with app.test_client() as client:
            res = client.post('/submit-score', json={
                'score': '21'
            })
            data = json.loads(res.get_data(as_text=True))
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['is_high_score'], True)
            res = client.post('/submit-score', json={
                'score': '14'
            })
            data = json.loads(res.get_data(as_text=True))
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['is_high_score'], False)
    def setUp(self):
        print('Set up')
    def tearDown(self):
        print('Tear down')
    @classmethod
    def setUpClass(cls):
        boggle_game = Boggle()
        boggle_board = boggle_game.make_board()
    @classmethod
    def tearDownClass(cls):
        print('tear down class')

class UnitTests(TestCase):
    def test_root_url(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<title>Boggle</title>", html) 
    def test_submit_guess(self):
        with app.test_client() as client:
            res = client.post('/submit-guess', json={
                'guess': 'word'
            })
            data = json.loads(res.get_data(as_text=True))
            self.assertEqual(res.status_code, 200)
            self.assertIn(data['Result'], {'not-on-board','not-a-word','ok'}) 
    def test_submit_score(self):
        with app.test_client() as client:
            res = client.post('/submit-score', json={
                'score': '21'
            })
            data = json.loads(res.get_data(as_text=True))
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['is_high_score'], True)
            res = client.post('/submit-score', json={
                'score': '14'
            })
            data = json.loads(res.get_data(as_text=True))
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['is_high_score'], False)
    def setUp(self):
        print('Set up')
    def tearDown(self):
        print('Tear down')
    @classmethod
    def setUpClass(cls):
        boggle_game = Boggle()
        boggle_board = boggle_game.make_board()
    @classmethod
    def tearDownClass(cls):
        print('tear down class')
