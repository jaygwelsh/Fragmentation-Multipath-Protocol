# fmp/routing.py

import random
import time
import threading
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Router:
    def __init__(self, paths):
        """
        Initialize with a list of paths.
        Each path is a tuple of (IP, port).
        """
        self.paths = {path: {'latency': float('inf'), 'score': 0.0, 'active': True} for path in paths}
        self.lock = threading.Lock()
        self.score_paths()

    def score_paths(self):
        """
        Simulate scoring paths based on latency.
        In a real implementation, actual latency probing would be performed.
        """
        for path in self.paths:
            latency = self._probe_path_latency(path)
            with self.lock:
                self.paths[path]['latency'] = latency
                self.paths[path]['score'] = 1.0 / (latency + 1e-6)  # Avoid division by zero
            logger.debug(f"Path {path} scored with latency {latency:.3f}s and score {self.paths[path]['score']:.6f}")

    def _probe_path_latency(self, path):
        """
        Simulate latency probing.
        Replace with real latency measurement in production.
        """
        simulated_latency = random.uniform(0.01, 0.1)  # Simulated latency between 10ms to 100ms
        time.sleep(simulated_latency)  # Simulate probing delay
        return simulated_latency

    def send_fragment(self, fragment):
        """
        Send fragment through the best scored active path.
        If the best path fails, fallback to the next best path.
        """
        with self.lock:
            sorted_paths = sorted(self.paths.items(), key=lambda item: item[1]['score'], reverse=True)
            for path, metrics in sorted_paths:
                if metrics['active']:
                    selected_path = path
                    break
            else:
                logger.error("No active paths available to send fragment.")
                return

        threading.Thread(target=self._send, args=(fragment, selected_path), daemon=True).start()

    def _send(self, fragment, path):
        """
        Simulate sending fragment.
        Replace with actual network transmission in production.
        """
        try:
            # Simulated send delay based on path latency
            time.sleep(self.paths[path]['latency'])
            # Here you would implement actual send logic, e.g., socket transmission
            # For MVP, we simulate successful send
            logger.info(f"Sent fragment via {path} with latency {self.paths[path]['latency']:.3f}s")
        except Exception as e:
            logger.error(f"Failed to send fragment via {path}: {e}")
            with self.lock:
                self.paths[path]['active'] = False  # Mark path as inactive on failure
            # Optionally, trigger re-scoring of paths
            self.score_paths()
