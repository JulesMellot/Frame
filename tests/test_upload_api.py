import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import json

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestUploadAPI(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.env_file = os.path.join(self.test_dir, ".env")
        self.web_dir = os.path.join(self.test_dir, "OnWeb")

        # Create directories
        os.makedirs(self.web_dir, exist_ok=True)

        # Create a minimal .env file for testing
        with open(self.env_file, "w") as f:
            f.write("API_TOKEN=test_token\n")

        # Set the environment variables
        os.environ["ENV_FILE"] = self.env_file

    def tearDown(self):
        # Clean up the environment variables
        if "ENV_FILE" in os.environ:
            del os.environ["ENV_FILE"]

        # Clean up the temporary directory
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch("dashboard.is_configured")
    @patch("frame.display.EPD_AVAILABLE", False)
    def test_upload_url_route_exists(self, mock_is_configured):
        """Test that the upload_url route is defined"""
        mock_is_configured.return_value = True

        import dashboard

        # Check that the route is defined
        routes = [rule.rule for rule in dashboard.app.url_map.iter_rules()]
        self.assertIn("/api/upload_url", routes, "Route /api/upload_url is not defined")

    @patch("dashboard.is_configured")
    @patch("frame.display.EPD_AVAILABLE", False)
    def test_upload_url_route_method(self, mock_is_configured):
        """Test that the upload_url route accepts POST method"""
        mock_is_configured.return_value = True

        import dashboard

        # Check that the route accepts POST method
        rules = [rule for rule in dashboard.app.url_map.iter_rules() if rule.rule == "/api/upload_url"]
        self.assertEqual(len(rules), 1, "Route /api/upload_url not found")
        self.assertIn("POST", rules[0].methods, "Route /api/upload_url does not accept POST method")


if __name__ == "__main__":
    unittest.main()
