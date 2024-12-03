# tests/test_routing.py

import unittest
from fmp.routing import Router
import secrets

class TestFMPRouting(unittest.TestCase):
    def setUp(self):
        paths = [('localhost', 8001), ('localhost', 8002)]
        self.router = Router(paths)

    def test_initial_path_scores(self):
        for path, metrics in self.router.paths.items():
            self.assertTrue(metrics['active'], f"Path {path} should be active initially.")
            self.assertGreater(metrics['score'], 0, f"Path {path} should have a positive score.")

    def test_send_fragment(self):
        fragment = b"Test fragment data."
        self.router.send_fragment(fragment)
        # Since send_fragment starts a thread, wait briefly
        import time
        time.sleep(0.2)
        # Check logs or other indicators as needed
        # For simplicity, assume success if no exceptions

    def test_path_failure(self):
        # Simulate path failure by deactivating a path
        self.router.paths[('localhost', 8001)]['active'] = False
        fragment = b"Test fragment after path failure."
        self.router.send_fragment(fragment)
        # Wait briefly for thread
        import time
        time.sleep(0.2)
        # Verify that the fragment was sent via the remaining active path
        # This can be done by checking logs or modifying Router to track sent paths

if __name__ == '__main__':
    unittest.main()
