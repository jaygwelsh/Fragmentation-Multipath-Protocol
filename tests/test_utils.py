# tests/test_utils.py

from unittest.mock import Mock

def mock_thread(target, args=(), kwargs=None, daemon=None):
    """
    Mocks threading.Thread by returning a mock object with a start method
    that executes the target function synchronously.
    """
    thread = Mock()
    thread.start.side_effect = lambda: target(*args, **(kwargs or {}))
    return thread
