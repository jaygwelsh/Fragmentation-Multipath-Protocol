# fmp/core.py

import msgpack
import secrets
import logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class FMPCore:
    def __init__(self, fragment_size=100, master_key=None, nonce_generator=None):
        """
        Initialize FMPCore with fragment size, master key, and nonce generator.
        """
        self.fragment_size = fragment_size
        self.master_key = master_key or secrets.token_bytes(32)  # 256-bit key
        self.aesgcm = AESGCM(self.master_key)
        self.nonce_generator = nonce_generator or (lambda: secrets.token_bytes(12))
        # Note: Nonce will be generated per fragment to ensure uniqueness

    def fragment_and_encrypt(self, data):
        """
        Fragment the data and encrypt each fragment.
        """
        if not data:
            logger.debug("No data to fragment and encrypt. Returning empty list.")
            return []

        # Fragment data
        fragments = [
            data[i:i+self.fragment_size] for i in range(0, len(data), self.fragment_size)
        ]
        encrypted_fragments = [
            self._encrypt_fragment(frag, i, len(fragments)) for i, frag in enumerate(fragments)
        ]
        logger.debug(f"Fragmented data into {len(fragments)} fragments.")
        return encrypted_fragments

    def _encrypt_fragment(self, fragment, index, total):
        """
        Encrypt a single fragment with metadata.
        Structure: nonce (12 bytes) + ciphertext
        """
        metadata = {'id': index, 'total': total}
        packed_metadata = msgpack.packb(metadata)
        metadata_length = len(packed_metadata)
        
        if metadata_length > 65535:
            raise ValueError("Metadata too large to encode in 2 bytes.")
        
        # Pack metadata length as 2-byte unsigned integer (big endian)
        metadata_length_bytes = metadata_length.to_bytes(2, 'big')
        
        nonce = self.nonce_generator()
        plaintext = metadata_length_bytes + packed_metadata + fragment
        ciphertext = self.aesgcm.encrypt(nonce, plaintext, None)
        logger.debug(f"Encrypted fragment {index} with nonce {nonce.hex()}.")
        # Prepend nonce to ciphertext for decryption
        return nonce + ciphertext

    def decrypt_and_reassemble(self, encrypted_fragments):
        """
        Decrypt and reassemble the original data from encrypted fragments.
        """
        if not encrypted_fragments:
            logger.debug("No fragments to reassemble. Returning empty data.")
            return b''

        fragments = {}
        total = None
        for idx, encrypted in enumerate(encrypted_fragments):
            try:
                nonce = encrypted[:12]
                ciphertext = encrypted[12:]
                decrypted = self.aesgcm.decrypt(nonce, ciphertext, None)
                
                if len(decrypted) < 2:
                    raise ValueError("Decrypted data is too short to contain metadata length.")
                
                # Extract metadata length
                metadata_length = int.from_bytes(decrypted[:2], 'big')
                if len(decrypted) < 2 + metadata_length:
                    raise ValueError("Decrypted data is too short to contain full metadata.")
                
                # Unpack metadata
                packed_metadata = decrypted[2:2 + metadata_length]
                metadata = msgpack.unpackb(packed_metadata)
                
                # Extract fragment data
                data = decrypted[2 + metadata_length:]
                
                fragments[metadata['id']] = data
                total = metadata['total']
                logger.debug(f"Decrypted fragment {metadata['id']} of {metadata['total']} (Fragment {idx}).")
            except Exception as e:
                logger.error(f"Failed to decrypt fragment {idx}: {e}")
                raise ValueError("Malformed or corrupted fragment detected.")

        if total is None:
            logger.error("No fragments received.")
            raise ValueError("No fragments received.")

        if len(fragments) != total:
            missing = set(range(total)) - set(fragments.keys())
            logger.error(f"Missing fragments: {missing}")
            raise ValueError(f"Missing fragments: {missing}")

        # Reassemble data in order
        try:
            reassembled = b''.join(fragments[i] for i in range(total))
        except KeyError as e:
            logger.error(f"Missing fragment {e.args[0]} during reassembly.")
            raise ValueError(f"Missing fragment {e.args[0]} during reassembly.")
        
        logger.debug("Successfully reassembled data.")
        return reassembled
