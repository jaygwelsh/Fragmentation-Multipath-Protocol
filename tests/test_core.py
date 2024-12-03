# tests/test_core.py

import unittest
from fmp.core import FMPCore
import secrets

class TestFMPCore(unittest.TestCase):
    def setUp(self):
        fragment_size = 100
        self.master_key = secrets.token_bytes(32)  # Securely generate a master key
        nonce_gen = (secrets.token_bytes(12) for _ in range(10000))
        self.core = FMPCore(
            fragment_size=fragment_size,
            master_key=self.master_key,
            nonce_generator=lambda: next(nonce_gen)
        )

    def test_empty_data(self):
        """
        Test that decrypt_and_reassemble returns empty data when no fragments are provided.
        """
        # Encrypt empty data
        encrypted_fragments = self.core.fragment_and_encrypt(b'')
        # Decrypt and reassemble
        decrypted_data = self.core.decrypt_and_reassemble(encrypted_fragments)
        # Assert that decrypted data is empty
        self.assertEqual(decrypted_data, b'', "Decrypted data should be empty for empty input data.")

    def test_single_fragment(self):
        """
        Test that a single fragment is correctly decrypted and reassembled.
        """
        data = b"Single fragment test data."
        encrypted_fragments = self.core.fragment_and_encrypt(data)
        decrypted_data = self.core.decrypt_and_reassemble(encrypted_fragments)
        self.assertEqual(decrypted_data, data, "Decrypted data does not match original data.")

    def test_multiple_fragments(self):
        """
        Test that multiple fragments are correctly decrypted and reassembled.
        """
        data = b"Multiple fragments test data." * 10  # Ensure multiple fragments
        encrypted_fragments = self.core.fragment_and_encrypt(data)
        decrypted_data = self.core.decrypt_and_reassemble(encrypted_fragments)
        self.assertEqual(decrypted_data, data, "Decrypted data does not match original data.")

    def test_corrupted_fragment(self):
        """
        Test that decrypt_and_reassemble raises ValueError when a fragment is corrupted.
        """
        data = b"Corrupted fragment test data."
        encrypted_fragments = self.core.fragment_and_encrypt(data)
        # Corrupt the first fragment by altering its bytes
        corrupted_fragment = bytearray(encrypted_fragments[0])
        corrupted_fragment[-1] ^= 0xFF  # Flip the last byte
        encrypted_fragments[0] = bytes(corrupted_fragment)
        # Attempt to decrypt and reassemble
        with self.assertRaises(ValueError) as context:
            self.core.decrypt_and_reassemble(encrypted_fragments)
        self.assertIn("Malformed or corrupted fragment detected", str(context.exception))

    def test_missing_fragment(self):
        """
        Test that decrypt_and_reassemble raises ValueError when a fragment is missing.
        """
        data = b"Missing fragment test data." * 10  # Ensure multiple fragments
        encrypted_fragments = self.core.fragment_and_encrypt(data)
        # Remove one fragment to simulate missing fragment
        incomplete_fragments = encrypted_fragments[:-1]  # Remove the last fragment
        # Attempt to decrypt and reassemble
        with self.assertRaises(ValueError) as context:
            self.core.decrypt_and_reassemble(incomplete_fragments)
        self.assertIn("Missing fragments", str(context.exception))

if __name__ == '__main__':
    unittest.main()
