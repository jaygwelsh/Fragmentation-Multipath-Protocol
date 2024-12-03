
import os
import time
import threading
from fmp.protocol import FMPProtocol

# Initialize a global list to store results
results = []

def scalability_test():
    print("\n--- Running Scalability Test ---\n")
    payload_sizes = [100_000, 1_000_000, 10_000_000]  # 100 KB, 1 MB, 10 MB
    fragment_sizes = [512, 1024, 2048]  # Fragment sizes in bytes

    for payload_size in payload_sizes:
        for fragment_size in fragment_sizes:
            try:
                data = b"A" * payload_size
                protocol = FMPProtocol(fragment_size=fragment_size, paths=[('localhost', 8001)])

                # Measure time taken for encryption and decryption
                start_time = time.time()
                encrypted_fragments = protocol.core.fragment_and_encrypt(data)
                protocol.core.decrypt_and_reassemble(encrypted_fragments)
                end_time = time.time()

                elapsed_time = end_time - start_time
                # Append result
                results.append({
                    "test": "Scalability",
                    "payload_size": payload_size,
                    "fragment_size": fragment_size,
                    "time_taken": elapsed_time
                })
            except Exception as e:
                print(f"Error during scalability test for payload={payload_size}, fragment_size={fragment_size}: {e}")

def concurrency_test():
    print("\n--- Running Concurrency Test ---\n")

    def sender_task(data, fragment_size):
        protocol = FMPProtocol(fragment_size=fragment_size, paths=[('localhost', 8001)])
        protocol.send_data(data)

    payload_size = 1_000_000  # 1 MB
    fragment_size = 1024
    threads = []

    try:
        start_time = time.time()

        # Create and start multiple threads
        for _ in range(10):  # Simulate 10 concurrent senders
            thread = threading.Thread(target=sender_task, args=(b"A" * payload_size, fragment_size))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Append result
        results.append({
            "test": "Concurrency",
            "payload_size": payload_size,
            "threads": 10,
            "fragment_size": fragment_size,
            "time_taken": elapsed_time
        })
    except Exception as e:
        print(f"Error during concurrency test: {e}")

def save_summary_to_file():
    # File path for results
    output_file = os.path.join(os.getcwd(), "benchmark_results.txt")

    with open(output_file, "w") as file:
        file.write("--- Benchmark Results Summary ---\n\n")
        if not results:
            file.write("No results to display. Ensure tests have been executed.\n")
        else:
            for result in results:
                if result["test"] == "Scalability":
                    file.write(f"[Scalability Test] Payload: {result['payload_size']} bytes | "
                               f"Fragment Size: {result['fragment_size']} bytes | "
                               f"Time: {result['time_taken']:.4f} seconds\n")
                elif result["test"] == "Concurrency":
                    file.write(f"[Concurrency Test] Payload: {result['payload_size']} bytes | "
                               f"Threads: {result['threads']} | "
                               f"Fragment Size: {result['fragment_size']} bytes | "
                               f"Time: {result['time_taken']:.4f} seconds\n")
        file.write("\n--- End of Summary ---\n")
    print(f"\nSummary saved to {output_file}")

if __name__ == "__main__":
    try:
        print("Starting benchmark tests...")
        scalability_test()
        print("\nScalability test completed.\n")
    except Exception as e:
        print(f"Error during scalability test: {e}")

    try:
        concurrency_test()
        print("\nConcurrency test completed.\n")
    except Exception as e:
        print(f"Error during concurrency test: {e}")

    print("\nSaving summary to file...\n")
    save_summary_to_file()
