# fmp/scripts/receiver.py

import logging
import sys
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
    master_key = b'0' * 32  # Ensure sender uses the same key

    protocol = FMPProtocol(
        fragment_size=fragment_size,
        paths=[('localhost', 8001), ('localhost', 8002)],
        master_key=master_key
    )
    
    # Simulate receiving data
    # In a real scenario, you'd receive encrypted fragments over the network
    # For benchmarking, we'll assume encrypted_fragments are already available
    # Here, we'll use a placeholder for demonstration
    
    # Example encrypted_fragments (should be received from the sender)
    # For demonstration, this will not work as there's no actual sending
    # In practice, implement network receiving logic here
    
    # decrypted_data = protocol.receive_data(encrypted_fragments)
    # logger.info(f"Received Data: {decrypted_data}")

    logger.info("Receiver is set up and ready to receive data.")

if __name__ == "__main__":
    main()
