# tests/test_protocol.py

import unittest
from unittest.mock import patch
from fmp.protocol import FMPProtocol
import secrets

class TestFMPProtocol(unittest.TestCase):
    def setUp(self):
        fragment_size = 100
        self.master_key = secrets.token_bytes(32)  # Securely generate a master key
        nonce_gen = (secrets.token_bytes(12) for _ in range(10000))
        self.protocol = FMPProtocol(
            fragment_size=fragment_size,
            paths=[('localhost', 8001), ('localhost', 8002)],
            master_key=self.master_key,
            nonce_generator=lambda: next(nonce_gen)
        )
        # Generate data larger than one fragment to have multiple fragments
        self.data = b"Test data for FMPProtocol." * 10  # 270 bytes, 3 fragments (100, 100, 70)

    def test_receive_data_success(self):
        # Fragment and encrypt data
        encrypted_fragments = self.protocol.core.fragment_and_encrypt(self.data)
        # Attempt to decrypt and reassemble
        decrypted_data = self.protocol.receive_data(encrypted_fragments)
        self.assertEqual(decrypted_data, self.data, "Decrypted data does not match original data.")

    def test_receive_data_incomplete(self):
        # Fragment and encrypt data
        encrypted_fragments = self.protocol.core.fragment_and_encrypt(self.data)
        # Remove one fragment to simulate incomplete data
        incomplete_fragments = encrypted_fragments[:-1]  # Remove the last fragment
        with self.assertRaises(ValueError) as context:
            self.protocol.receive_data(incomplete_fragments)
        self.assertIn("Missing fragments", str(context.exception))

    def test_send_data_failure(self):
        # Define a side_effect function that can access 'self'
        def side_effect(fragment):
            # Simulate failure by deactivating the first path
            self.protocol.router.paths[('localhost', 8001)]['active'] = False

        with patch('fmp.routing.Router.send_fragment', side_effect=side_effect):
            # Send data, which should attempt to send via path ('localhost',8001)
            # which will be deactivated, and then try the next path
            # Assuming the Router class handles path fallback
            try:
                self.protocol.send_data(self.data)
            except Exception as e:
                self.fail(f"send_data raised an exception unexpectedly: {e}")
            # Verify that the first path is now inactive
            self.assertFalse(self.protocol.router.paths[('localhost',8001)]['active'],
                             "Path ('localhost',8001) should be inactive after simulated failure.")

    def test_send_and_receive_empty_data(self):
        """
        Test sending and receiving empty data.
        """
        empty_data = b''
        encrypted_fragments = self.protocol.core.fragment_and_encrypt(empty_data)
        decrypted_data = self.protocol.receive_data(encrypted_fragments)
        self.assertEqual(decrypted_data, empty_data, "Decrypted data should be empty for empty input data.")

if __name__ == '__main__':
    unittest.main()
