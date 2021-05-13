import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movies,setup_db,Actors,db_drop_and_create_all
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgres://postgres:123qwe@localhost:5432/capstone"
        setup_db(self.app, self.database_path)
        self.EXECUTIVE_PRODUCER = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5pLXZjalItX1dWdElGbWhETzJwVCJ9.eyJpc3MiOiJodHRwczovL3Byb2plY3QzLWZ1bGwtc3RhY2sudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNGRkMzc3Yzg0NDFjMDA2OTZjODY4MyIsImF1ZCI6IjUwMDAiLCJpYXQiOjE2MTY4ODYxNjAsImV4cCI6MTYxNjk3MjU2MCwiYXpwIjoiNDlCZTg2eUpkRDVyWVdmUFdmNnJVaHpkVGl3eElNSVIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.k6AF1fkyHEgm6I5-YX-D8VRLY5cyV3Djq71vlwS0O7KiduI8mXtHCpNKyAow6gmPxwxzWXcrx76SE6pHocUPYuMihi8yBbLOIfbGF7DbdAAOZvBt8TnWmWkUd_7lsHQNd7_6NGGBSfrAqcR_9Vxv6IUjbhfdtsH0Qdt7MvTnEWYHmi8CJpK1MYg-X51zAlT-iP8MqS-uEombiVVtcXgds1QF_3VsjDB1w5vvDD3sPR-JIizVWEB75cQj1YCZ4eZT35hA1-BO8zfSxPqzKnTDezK-DjLAHHdZSwqHZguuwbYNYeWQIRYu1MwHm4xHtknBVjpcFRkaucSr9FZKG7Exdw"

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
##GET
    def test_get_200_movies(self):
        res = self.client().get("/movies", headers={
			"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_get_200_actors(self):
        res = self.client().get("/actors", headers={
			"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
##CREATE
    def test_create_movies(self):
        res = self.client().post("/movies",json={"title":"1",
                                                "release_date":"2"
                                                }, 
                                                headers={"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
    def test_create_actors(self):
        res = self.client().post("/actors",json={
                                                "name":"1",
                                                "age":"2",
                                                "gender":"1"
                                                }, 
                                                headers={"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
##PATCH 
    # def test_patch_actors(self):
    #     res = self.client().patch("/actors/1",json={"name":"9",
    #                                             "age":"9",
    #                                             "gender":"9"
    #                                             }, 
    #                                             headers={"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'], True)
    def test_404_patch_actors(self):
        res = self.client().patch("/actors/9999",json={"name":"9",
                                                "age":"9",
                                                "gender":"9"
                                                }, 
                                                headers={"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])

    # def test_patch_movies(self):
    #     res = self.client().patch("/movies/1",json={"title":"9",
    #                                             "release_date":"9"
    #                                             }, 
    #                                             headers={"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'], True)
    def test_404_patch_movies(self):
        res = self.client().patch("/movies/9999",json={"title":"9",
                                                "release_date":"9"
                                                }, 
                                                headers={"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])
##DELETE
    def test_delete_movies(self):
        res = self.client().delete("/movies/1", headers={
            "Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_delete_404_movies(self):
        res = self.client().delete("/movies/9999",headers={
			"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertFalse(data["success"])
        self.assertEqual(data['error'], 404)

	def test_delete_actors(self):
        res = self.client().delete("/actors/1", headers={
            "Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        
     def test_delete_404_actors(self):
        res = self.client().delete("/actors/9999",headers={
			"Authorization": "Bearer {}".format(self.EXECUTIVE_PRODUCER)})
        data = json.loads(res.data)
        self.assertFalse(data["success"])
        self.assertEqual(data['error'], 404)

if __name__ == "__main__":
    unittest.main()