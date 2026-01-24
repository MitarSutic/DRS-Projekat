import time

MAX_ATTEMPTS = 3
BLOCK_TIME = 15  

_failed_attempts = {}
_blocked_until = {}


def is_blocked(email: str) -> bool:
    if email not in _blocked_until:
        return False

    if time.time() > _blocked_until[email]:
        del _blocked_until[email]
        _failed_attempts.pop(email, None)
        return False

    return True


def register_failed_attempt(email: str):
    _failed_attempts[email] = _failed_attempts.get(email, 0) + 1

    if _failed_attempts[email] >= MAX_ATTEMPTS:
        _blocked_until[email] = time.time() + BLOCK_TIME


def reset_attempts(email: str):
    _failed_attempts.pop(email, None)
    _blocked_until.pop(email, None)