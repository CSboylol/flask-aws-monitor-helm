import unittest

from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page_returns_success(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AWS Resource Viewer", response.data)


if __name__ == "__main__":
    unittest.main()