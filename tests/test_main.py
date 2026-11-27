import unittest

from app.main import app


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_search_returns_matching_user(self):
        response = self.client.get("/search", query_string={"username": "demo-user"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"results": [["demo-user"]]})

    def test_search_treats_sql_syntax_as_username_data(self):
        response = self.client.get(
            "/search",
            query_string={"username": "' OR '1'='1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"results": []})


if __name__ == "__main__":
    unittest.main()
