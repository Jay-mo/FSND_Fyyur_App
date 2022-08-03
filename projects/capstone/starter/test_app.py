
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies
from dateutil.parser import parse


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        database_username = os.getenv('DBUSER')
        database_password = os.getenv('DBPASS')
        self.database_path = "postgresql://{}:{}@{}/{}".format(database_username, database_password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            new_movie = Movies("Transformers", parse("July 3, 2007"))
            new_actor = Actors("Jason Kent Bateman",43,"Male")
            self.db.session.add(new_movie)
            self.db.session.add(new_actor)
            self.db.session.commit()

        self.test_movie = {
                        "title": "Sweet November",
                        "release_date": parse("February 16, 2001")
                    }

        self.patch_movie = {
                        "title": "Captain America",
                        "release_date": parse("May 16, 2006")
                    }

        self.test_actor = {
                        "name": "Keanu Reeves",
                        "age": "57",
                        "gender": "Male"
                    }

        self.patch_actor = {
                        "name": "Charlize Theron",
                        "age": "43",
                        "gender": "Female"
                    }

        self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNWYzVhSkVMamIyS0ZjcTJZWVFtQiJ9.eyJpc3MiOiJodHRwczovL21vdmllLWFwcC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MjJhNDE2M2ExNzEyYTAwNjk5ZTk4Y2YiLCJhdWQiOiJtb3ZpZS1hcHAtZnNuZC1hcGkiLCJpYXQiOjE2NDcwMTczNTQsImV4cCI6MTY0NzAyNDU1NCwiYXpwIjoibUcwV25FOG1kbUlFaW9sYUkweXVycjgwTG83dkRjdUQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3IiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWUiLCJyZWFkOm1vdmllcyJdfQ.e0viLXQsQNzRfRrIcn1kQvd7t89YlIwPytkoNFALf49IQ0H8yDr-MI19vMQ21iT5vMCBfbZNLUyBYcsYWwe2kZg13TjFT7QcZZQVO_jHFzNRVSILqUUMYz0q6K7xSNTpQhBpVdSEIEstFPfeQLQTWNQEBKOO2xqRo7dGHiz7VLRTIzYNi3c3XRnnEZB574fEMvERw3CxdW3M_xG5HxbQuBI9xa-RsWWE2pN3QhwiMPhT8Tx6i-OhvwXnFp9DPSgnDU_JDsK3BCP93BHmSxmcOIoK9_BcRFnyaM-B1pXPNsFkJ8_noPMHdhd8df1pnr79gI9y8J2jpJoEh5h1YYAS0g"

        self.casting_assistant = {
            'token': "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNWYzVhSkVMamIyS0ZjcTJZWVFtQiJ9.eyJpc3MiOiJodHRwczovL21vdmllLWFwcC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MjJhNDE2M2ExNzEyYTAwNjk5ZTk4Y2YiLCJhdWQiOiJtb3ZpZS1hcHAtZnNuZC1hcGkiLCJpYXQiOjE2NTk0Njk4MjQsImV4cCI6MTY1OTU1NjIyNCwiYXpwIjoibUcwV25FOG1kbUlFaW9sYUkweXVycjgwTG83dkRjdUQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3IiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWUiLCJyZWFkOm1vdmllcyJdfQ.VuowCinPHNJxN8zE61L8JoXQFBoLMjuZ_GL1O4O-LduEcMUCtu2CLiW4mXKUgRfPtEKLOHAip7jjXsFozYTmQ9fxXn5ZxZi7LSvoF8dSPbt8oVjgMEBSJ5C63W_EjECgipy4-Y-pwhkTg0sTXZi2x6uLdr1-GrunOonmJkBtZPL3NHLLjO-KvYP9wkTb-lUevwBnNUXhMGSYCGbj966YV8OVIFPjPVaZsi0lew0AUjCA0wyKYDnWCZ7ZyKYf3nmxW2DP7q3imqMo2yWGqDwHxkR0KcBbQCEh5XLwQbsBN_gi7_7QAlEufhNV9eNoE-MDhbMGjmeGI2ehDfcwDLi72g"
        }

        self.casting_director = {
            'token': "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNWYzVhSkVMamIyS0ZjcTJZWVFtQiJ9.eyJpc3MiOiJodHRwczovL21vdmllLWFwcC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MjJhNDUxZjYzNzY3ZTAwNzA0ZDliY2EiLCJhdWQiOiJtb3ZpZS1hcHAtZnNuZC1hcGkiLCJpYXQiOjE2NTk0NzExNzQsImV4cCI6MTY1OTU1NzU3NCwiYXpwIjoibUcwV25FOG1kbUlFaW9sYUkweXVycjgwTG83dkRjdUQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsIm1vZGlmeTphY3RvciIsIm1vZGlmeTptb3ZpZSIsInBvc3Q6YWN0b3IiLCJyZWFkOmFjdG9yIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllIiwicmVhZDptb3ZpZXMiXX0.i-mKqyn3X9OPyJ7r360DCvNPYZDG_DoiRPA7jqJB09GDZSVhHfkt_JJ6J0CKkWp7NiALjD6s_qi7K02SLse5t1OZImXtKOodwOiO5gOhEjmjVfGfQOO5yo8xahIvgaPkXLUJU_JpmbMhQUeFbsxdK1Unw4AR0MlJpHsEtmVOwD-nASVT-6SYg0JIeA_mxIiIz1Z6oGU_jj9Wah13F-QscGRhzbbIV0TV0LM-Xw-r3esDfwcBB97veUp-0gVnrTaSONRheKqRogcpcu2oKD2fzjMnpqvP1pYCvqOUljurUMz6hf99nlaYZz757bQjZipy88rVqKoTW0uEqtetCuniGQ"
        }

        self.executive_director = {
            'token': "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNWYzVhSkVMamIyS0ZjcTJZWVFtQiJ9.eyJpc3MiOiJodHRwczovL21vdmllLWFwcC1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmRjNDczMDU4NmQ4Y2Q2N2QxNzYyZTkiLCJhdWQiOiJtb3ZpZS1hcHAtZnNuZC1hcGkiLCJpYXQiOjE2NTk0NzEwNDMsImV4cCI6MTY1OTU1NzQ0MywiYXpwIjoibUcwV25FOG1kbUlFaW9sYUkweXVycjgwTG83dkRjdUQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsIm1vZGlmeTphY3RvciIsIm1vZGlmeTptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIiwicmVhZDphY3RvciIsInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZSIsInJlYWQ6bW92aWVzIl19.UMCxc9CSiY8YdYCoVLE9pYwuPYTMU6r4PTh7zFltCuT-EI_T_pZNxNQ5CVuepG988uB1wGBYnlZlPokCixXj7B3UhfAHEcsQsXT3zS9urnWfEa06cEmjDBSTjXP1qQAKvb1bno1X9eGFmswxqY9kzs_8QCFDXvBUBVYaOcv-g9SfDf-n2fj95n8EjcLfhRvNJ0JupesOgRHUf4ck1K88MAJ9eyURzGYtuyHQlxvCw14lqDNupgoeSFLrI8jNHWwYfKEhObQ6_NNXOs22Blhv3dtBO-WBg08W4hVsHCUj9IhiTlXmN1tK2h7dukOQU0Wxl96TC3N3B9fWYvuEVbcKMg"
        }

        




    def tearDown(self):
        """Executed after reach test"""
        
        with self.app.app_context():
            self.db.drop_all()

        
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_movies(self):
        res = self.client().get("/movies", headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant['token'])
            })
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)



    def test_get_all_movies_without_authorization(self):
        res = self.client().get("/movies")
        data = res.json
        
        self.assertEqual(res.status_code, 401)


    def test_get_all_actors(self):
        res = self.client().get("/actors", headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant['token'])
            })
        data = res.json

        expected_ouput = {
                            "age": 43,
                            "gender": "Male",
                            "id": 1,
                            "name": "Jason Kent Bateman"
                        }

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)



    def test_get_all_actors_without_authorization(self):
        res = self.client().get("/actors")
        data = res.json
        
        self.assertEqual(res.status_code, 401)


    def test_post_movie(self):

        res = self.client().post("/movies", json=self.test_movie, headers={
                "Authorization":
                "Bearer {}".format(self.executive_director['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 200)


    def test_post_movie_without_auth(self):

        res = self.client().post("/movies", json=self.test_movie)
        data = res.data
        

        self.assertEqual(res.status_code, 401)

    def test_post_movie_with_wrong_auth(self):

        res = self.client().post("/movies", json=self.test_movie , headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 403)


    def test_post_actor(self):

        res = self.client().post("/actors", json=self.test_actor, headers={
                "Authorization":
                "Bearer {}".format(self.executive_director['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 200)


    def test_post_actor_without_auth(self):

        res = self.client().post("/actors", json=self.test_movie)
        data = res.data
        

        self.assertEqual(res.status_code, 401)

    def test_post_actor_with_wrong_auth(self):

        res = self.client().post("/actors", json=self.test_actor , headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 403)

    
    def test_delete_movie(self):

        res = self.client().delete("/movies/2", headers={
                "Authorization":
                "Bearer {}".format(self.executive_director['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 200)


    def test_delete_movie_without_auth(self):

        res = self.client().delete("/movies/2" )
        data = res.data
        

        self.assertEqual(res.status_code, 401)

    def test_delete_movie_with_wrong_auth(self):

        res = self.client().delete("/movies/2", headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 403)


    def test_patch_movie(self):

        res = self.client().patch("/movies/1", json=self.patch_movie, headers={
                "Authorization":
                "Bearer {}".format(self.executive_director['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 200)


    def test_patch_movie_without_auth(self):

        res = self.client().delete("/movies/2" , json=self.patch_movie)
        data = res.data
        

        self.assertEqual(res.status_code, 401)

    def test_patch_movie_with_wrong_auth(self):

        res = self.client().delete("/movies/2",  json=self.patch_movie, headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 403)




    ############


    def test_delete_actor(self):

        res = self.client().delete("/actors/1", headers={
                "Authorization":
                "Bearer {}".format(self.executive_director['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 200)


    def test_delete_actor_without_auth(self):

        res = self.client().delete("/actor/2" )
        data = res.data
        

        self.assertEqual(res.status_code, 404)

    def test_delete_actors_with_wrong_auth(self):

        res = self.client().delete("/actors/1", headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 403)


    def test_patch_actors(self):

        res = self.client().patch("/actors/1", json=self.patch_actor, headers={
                "Authorization":
                "Bearer {}".format(self.executive_director['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 200)


    def test_patch_actors_without_auth(self):

        res = self.client().patch("/actors/1" , json=self.patch_actor)
        data = res.data
        

        self.assertEqual(res.status_code, 401)

    def test_patch_actor_with_wrong_auth(self):

        res = self.client().patch("/actors/1",  json=self.patch_actor, headers={
                "Authorization":
                "Bearer {}".format(self.casting_assistant['token'])})
        data = res.data
        

        self.assertEqual(res.status_code, 403)
        




    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()