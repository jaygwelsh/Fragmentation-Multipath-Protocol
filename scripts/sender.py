# fmp/scripts/sender.py

import logging
import sys
import secrets
from fmp.protocol import FMPProtocol

def main():
    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Initialize FMPProtocol
    fragment_size = 100
    master_key = b'0' * 32  # Ensure receiver uses the same key
    nonce_gen = (secrets.token_bytes(12) for _ in range(10000))  # Generator for unique nonces

    protocol = FMPProtocol(
        fragment_size=fragment_size,
        paths=[('localhost', 8001), ('localhost', 8002)],
        master_key=master_key,
        nonce_generator=lambda: next(nonce_gen)
    )
    
    # Read data to send, for example from command-line argument or a file
    # Here, we'll use predefined data
    data = b"HelloWorldThisIsATest" * 1000  # Example data
    
    # Send data
    logger.info("Starting to send data...")
    protocol.send_data(data)
    logger.info("Data sent successfully.")

if __name__ == "__main__":
    main()
