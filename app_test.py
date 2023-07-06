import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie, db_drop_and_create_all
from sqlalchemy import desc
from datetime import date

# Create dict with Authorization key and Bearer token as values. 
# Later used by test classes as Header

casting_assistant_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3R051UnphMFdOMk9BY2ZCdXhVZyJ9.eyJpc3MiOiJodHRwczovL2FydGh1ci1kZXYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0YTcwYjVkYzhlN2Y0MjNjYjUyNWNiNCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjg4NjY5MzU0LCJleHAiOjE2ODg2NzY1NTQsImF6cCI6Im0xUlAxbk44bVJsVUJSRzVVdEw5a3dWbUVVMVlrRVRzIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.XrRFsFEqD1enqc0HxsAx0UwztnchLTeRg6bTBrDSqBnLPMlQtVFiLO8EZplPE5-LZBJRWSHWDvUvL02oEx1XJ9vSsDbh3tHeHth4aJCSA5ciOzmlsrzHVGyIwsG39cpDOFh6eDgO2XdP5kV3-s1Kx08vBQA_g8VqBDzevmWWCN0AeyF7USTLA08oGWZFM_jF_9j4nRrzLgEY0551OtZRV1DNPjw5pP43uj2qhksTgOssokQApRa_NaUYixD9xHc7sFl07CpYk385KSz6zg4vOe_ZPbEM1xlYdM3AjYGiXP4_pRTFJMivc0ruDEZmAbw_bZCtNvgcAT3INrOu1gicNw"
}

casting_director_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3R051UnphMFdOMk9BY2ZCdXhVZyJ9.eyJpc3MiOiJodHRwczovL2FydGh1ci1kZXYudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0OTJmODkwOGI4NWM4YTY5NDlmZjIwZSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjg4NjY5NDkxLCJleHAiOjE2ODg2NzY2OTEsImF6cCI6Im0xUlAxbk44bVJsVUJSRzVVdEw5a3dWbUVVMVlrRVRzIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.HhvDVgffjcz613ui2AOXjM1MaHhZvXw5zA9gn6lNuSNpet3qJ8sAUuzsDgeXg3EYCekofP6kPo2-mUHUT8kMKeADUD5bP4EujH8rM-OE_8j_qcUPP0YyL4Lq8y3srbf7FqXZQKhw1M_b5DW9XliCxtxnOPC_DcIMnBwJf-m9xY0DR4-Ht9sNiS-B_oFYBQJbxNfQrfKpCCBREd6Mttx3i2f0z68fW5uI8dvgpLcML0FE9fKj6GK9nAJyV10DErS6b8qyq-DBmxnbZwAKscNfqkoiv2qJUzz5YHAZ789kIbDq8w0kuyrqX63xMgjdPPg_vzf0l1zaQ8rVzgKO9sO66Q"
}

executive_producer_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inl3R051UnphMFdOMk9BY2ZCdXhVZyJ9.eyJpc3MiOiJodHRwczovL2FydGh1ci1kZXYudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTExMTMwNTYwMDg5MjkxMTk1NDQzIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2ODg2Njk1MjQsImV4cCI6MTY4ODY3NjcyNCwiYXpwIjoibTFSUDFuTjhtUmxVQlJHNVV0TDlrd1ZtRVUxWWtFVHMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.OH9hqGQ-oYskgKBhiAw756njN8sZ9mfYv2oID59EFPUUdoxN4uewD3g3ZdRLWKoLUlFjv5iR3Zw_HTUo1TZofZA1m54MT6yev-iE8p3Hk8MeAWlcwlu6XgtzBwHdme0fH-jk1kaxAYg3ovsTbNIPsAC1cIC1zZplKrMA7LVCDbgyw50apC6qba3OzwNPI0jeyPjn3y_fa9wYdqUTQD3mOG8mkhqBJ2XwWyeQP_4JG6kveKnYUN3QCrftU4Oz2lL3MG_IjteN4PTGvGO9v7aEUTskqzXmPmt9kmhOqKgBP_ZY06mJg3oxZZHgEddznePryWA6BeQuQO6SApnVsR8xkQ"
}


class capstoneTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_create_new_actor(self):
        """Test POST actor."""

        create_actor = {
            'name' : 'Junior',
            'gender': 'Male',
            'age' : 99, #A very old actor
            'movie_id':Movie.query.first().id
        } 
        res = self.client().post('/actors', json = create_actor, headers = casting_director_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)
    
    def test_error_401_new_actor(self):
        """Test POST new actor w/o Authorization."""

        json_create_actor = {
            'name' : 'Arthur',
            'age' : 25
        } 

        res = self.client().post('/actors', json = json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_422_create_new_actor(self):
        """Test Error POST actor."""

        json_create_actor_without_name = {
            'age' : 99
        } 

        res = self.client().post('/actors', json = json_create_actor_without_name, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'no name provided.')


    def test_get_all_actors(self):
        """Test GET all actors."""
        res = self.client().get('/actors?page=1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_all_actors(self):
        """Test GET all actors w/o Authorization."""
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_404_get_actors(self):
        res = self.client().get('/actors?page=6245672', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'No actors found!')


    def test_edit_actor(self):
        """Test PATCH existing actors"""
        json_edit_actor_with_new_age = {
            'age' : 90
        } 
        res = self.client().patch('/actors/1', json = json_edit_actor_with_new_age, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)

    def test_error_400_edit_actor(self):

            res = self.client().patch('/actors/624564', headers = casting_director_auth_header)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 400)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'] , 'No valid JSON body!')

    def test_error_404_edit_actor(self):
        json_edit_actor_with_new_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/624564', json = json_edit_actor_with_new_age, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Actor not found on DB!')


    def test_error_401_delete_actor(self):
        """Test DELETE existing actor w/o Authorization"""
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_actor(self):

        res = self.client().delete('/actors/1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actor(self):

        res = self.client().delete('/actors/1', headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_actor(self):

        res = self.client().delete('/actors/624562', headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Actor not found in database.')


    def test_create_new_movie(self):

        json_create_movie = {
            'title' : 'Old man movie',
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = json_create_movie, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    def test_error_422_create_new_movie(self):

        json_create_movie_without_name = {
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = json_create_movie_without_name, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Missing information')

    def test_get_all_movies(self):
        res = self.client().get('/movies?page=1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_error_401_get_all_movies(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_404_get_movies(self):
        res = self.client().get('/movies?page=7543246', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'no movies found in database.')

    def test_edit_movie(self):
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/1', json = json_edit_movie, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_error_400_edit_movie(self):
        res = self.client().patch('/movies/1', headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'request does not contain a valid JSON body.')

    def test_error_404_edit_movie(self):
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/4563475', json = json_edit_movie, headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Movie not found in database.')


    def test_error_401_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_movie(self):
        res = self.client().delete('/movies/1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_movie(self):
        res = self.client().delete('/movies/65436734', headers = executive_producer_auth_header) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Movie not found in database.')

# Make the tests conveniently executable.
# From app directory, run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()