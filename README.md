
# FMP (Fragmentation and Multipath Protocol)

**FMP** is a lightweight data transmission protocol designed for secure, efficient, and decentralized communication. It fragments data into dynamically sized pieces, encrypts them with robust cryptographic algorithms, and routes them through optimized multi-path channels. The protocol ensures low latency, robust tamper resistance, and scalability, making it ideal for applications requiring cutting-edge security and performance.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Sending Data](#sending-data)
  - [Receiving Data](#receiving-data)
- [File Structure](#file-structure)
- [Testing](#testing)
- [Benchmarking](#benchmarking)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Data Fragmentation:** Splits data into manageable fragments with metadata for reassembly.
- **Encryption:** Secures each fragment using authenticated encryption (AES-GCM) with unique nonces.
- **Adaptive Multi-Path Routing:** Routes fragments through dynamically scored paths for optimal delivery.
- **Reassembly:** Collects and reassembles fragments securely at the destination.
- **Error Handling:** Validates fragment integrity and handles missing fragments with high reliability.
- **Logging:** Provides detailed logs for monitoring and debugging.
- **Scalability:** Efficiently handles large data payloads and high-throughput scenarios.

---

## Installation

### Prerequisites

- **Python 3.7 or higher**: Ensure Python is installed. You can download it from [python.org](https://www.python.org/downloads/).
- **pip**: Python package installer. It usually comes with Python. Verify by running `pip --version`.

### Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/fmp.git
    cd fmp
    ```

2. **Create a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

---

## Usage

### Sending Data

1. **Start the Receiver:**

    On the destination machine or terminal, run the receiver script:

    ```bash
    python scripts/receiver.py
    ```

2. **Send Data from Sender:**

    On the source machine or another terminal, run the sender script:

    ```bash
    python scripts/sender.py
    ```

    **Example Code:**

    ```python
    from fmp.protocol import FMPProtocol

    # Define available paths (IP, port)
    paths = [('localhost', 8001), ('localhost', 8002)]

    # Initialize protocol
    protocol = FMPProtocol(fragment_size=1024, paths=paths)

    # Data to send
    data = b"Your data here..."

    # Send data
    protocol.send_data(data)
    ```

### Receiving Data

**Receiver Script Example (`scripts/receiver.py`):**

```python
from fmp.protocol import FMPProtocol

# Define available paths (IP, port)
paths = []  # Not used for receiving

# Initialize protocol
protocol = FMPProtocol(fragment_size=1024, paths=paths)

# Function to handle incoming fragments (to be integrated with actual network code)
def handle_incoming_fragment(encrypted_fragment):
    data = protocol.receive_data([encrypted_fragment])
    if data:
        print("Received Data:", data)

# Note: Integrate this with actual network listening code.
```

---

## File Structure

```
FMP/
├── fmp/
│   ├── __init__.py
│   ├── core.py              # Unified fragmentation, encryption, and reassembly
│   ├── routing.py           # Adaptive routing and path scoring
│   └── protocol.py          # Main protocol logic
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_protocol.py
│   └── test_routing.py
├── benchmarks/
│   ├── benchmark_latency.py
│   └── benchmark_throughput.py
├── scripts/
│   ├── sender.py            # Example sender script
│   └── receiver.py          # Example receiver script
├── README.md
├── requirements.txt
├── setup.py
├── LICENSE
└── .gitignore
```

---

## Testing

Run unit tests using `unittest`:

```bash
python -m unittest discover tests
```

---

## Benchmarking

### Latency Benchmark

Measure fragmentation and encryption latency:

```bash
python benchmarks/benchmark_latency.py
```

### Throughput Benchmark

Measure data throughput:

```bash
python benchmarks/benchmark_throughput.py
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a pull request.

Please ensure your code follows the project's coding standards and includes relevant tests.

---

## License

This project is licensed under the MIT License.
