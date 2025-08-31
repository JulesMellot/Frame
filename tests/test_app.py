import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import json

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.env_file = os.path.join(self.test_dir, '.env')
        
        # Create a minimal .env file for testing
        with open(self.env_file, 'w') as f:
            f.write("API_TOKEN=test_token\n")
        
        # Set the environment variable to point to our test .env file
        os.environ['ENV_FILE'] = self.env_file

    def tearDown(self):
        # Clean up the environment variable
        if 'ENV_FILE' in os.environ:
            del os.environ['ENV_FILE']
        
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch('dashboard.is_configured')
    def test_app_imports(self, mock_is_configured):
        """Test that the application can be imported without errors"""
        mock_is_configured.return_value = True
        try:
            import dashboard
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to import dashboard: {e}")

    @patch('dashboard.is_configured')
    def test_app_routes(self, mock_is_configured):
        """Test that the application routes are defined"""
        mock_is_configured.return_value = True
        import dashboard
        
        # Check that the main routes are defined
        routes = [rule.rule for rule in dashboard.app.url_map.iter_rules()]
        expected_routes = ['/', '/setup', '/api/upload', '/api/upload_url', '/api/function', '/api/tags', '/api/bantags', '/api/new', '/api/setup', '/api/token']
        
        for route in expected_routes:
            self.assertIn(route, routes, f"Route {route} is not defined")

    def test_config_loading(self):
        """Test that configuration loads correctly"""
        # We need to modify the path to import config properly
        import importlib
        import frame.config
        
        # Reload the config module to pick up our test .env file
        importlib.reload(frame.config)
        
        # Check that the API_TOKEN is loaded
        self.assertEqual(frame.config.API_TOKEN, 'test_token')

if __name__ == '__main__':
    unittest.main()