# fmp/protocol.py

import logging
import secrets
from fmp.core import FMPCore
from fmp.routing import Router

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class FMPProtocol:
    def __init__(self, fragment_size=100, paths=None, master_key=None, nonce_generator=None):
        """
        Initialize FMPProtocol with FMPCore and Router.
        """
        paths = paths or [('localhost', 8001), ('localhost', 8002)]
        master_key = master_key or FMPCore().master_key
        nonce_generator = nonce_generator or (lambda: secrets.token_bytes(12))
        self.core = FMPCore(
            fragment_size=fragment_size,
            master_key=master_key,
            nonce_generator=nonce_generator
        )
        self.router = Router(paths)
        logger.debug("Initialized FMPProtocol.")

    def send_data(self, data):
        """
        Fragment, encrypt, and send data via the router.
        """
        encrypted_fragments = self.core.fragment_and_encrypt(data)
        logger.debug(f"Sending {len(encrypted_fragments)} encrypted fragments.")
        for fragment in encrypted_fragments:
            self.router.send_fragment(fragment)

    def receive_data(self, encrypted_fragments):
        """
        Receive encrypted fragments and reassemble the original data.
        """
        return self.core.decrypt_and_reassemble(encrypted_fragments)
