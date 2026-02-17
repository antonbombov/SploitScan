import time

def retryit(func):
    """Re-request Decorator"""
    def wrapper(*args, **kwargs):

        result = None
        for delay in [0, 15, 25, 35, 45]:
            if delay > 0:
                print(f"Re-request with delay {delay}s")
                time.sleep(delay)
            result = func(*args, **kwargs)

            # Do I need to make a repeat request?
            need_retry = (
                    result is None or  # None
                    (isinstance(result, tuple) and result and result[0] is None) or  # (None, ...)
                    (isinstance(result, dict) and not result)  # empty dictionary {}
            )

            if not need_retry:
                break

        return result
    return wrapper