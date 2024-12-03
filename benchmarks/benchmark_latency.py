# benchmarks/benchmark_latency.py

import time
import secrets
from fmp.core import FMPCore
from fmp.protocol import FMPProtocol
import msgpack

def unique_nonce():
    return secrets.token_bytes(12)  # AES-GCM requires 96-bit (12-byte) nonces

def benchmark_latency():
    # Initialize FMPCore with adequate fragment_size
    fragment_size = 100  # 100 bytes data per fragment
    master_key = b'0' * 32  # Ensure this is consistent between sender and receiver
    nonce_gen = (unique_nonce() for _ in range(10000))  # Generator for unique nonces
    
    core = FMPCore(
        fragment_size=fragment_size,
        master_key=master_key,
        nonce_generator=lambda: next(nonce_gen)
    )
    protocol = FMPProtocol(
        fragment_size=fragment_size,
        paths=[('localhost', 8001), ('localhost', 8002)],
        master_key=master_key,
        nonce_generator=lambda: next(nonce_gen)
    )
    
    # Prepare data to send
    data = b'B' * (fragment_size * 1000)  # 1000 fragments, total 100,000 bytes
    
    # Fragment and encrypt
    start_fragment_time = time.time()
    encrypted_fragments = core.fragment_and_encrypt(data)
    fragmentation_time = time.time() - start_fragment_time
    print(f"Fragmented data into {len(encrypted_fragments)} fragments in {fragmentation_time:.4f} seconds.")
    
    # Simulate sending fragments
    # In a real scenario, you'd send the fragment over the network
    # For benchmarking, we'll skip actual sending
    
    # Simulate receiving fragments (for benchmarking, you might reassemble them)
    start_decrypt_time = time.time()
    try:
        decrypted_data = core.decrypt_and_reassemble(encrypted_fragments)
        decrypt_time = time.time() - start_decrypt_time
        print(f"Decrypted data length: {len(decrypted_data)} in {decrypt_time:.4f} seconds.")
        assert decrypted_data == data, "Decrypted data does not match original data."
        print("Data integrity verified: Decrypted data matches original data.")
    except ValueError as ve:
        decrypt_time = time.time() - start_decrypt_time
        print(f"Decryption failed after {decrypt_time:.4f} seconds: {ve}")
    except AssertionError as ae:
        decrypt_time = time.time() - start_decrypt_time
        print(f"Assertion Error after {decrypt_time:.4f} seconds: {ae}")

    total_time = fragmentation_time + decrypt_time
    print(f"Latency Benchmark Completed in {total_time:.2f} seconds.")

if __name__ == "__main__":
    benchmark_latency()
