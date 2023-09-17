import time
import logging

logger = logging.getLogger("skeleton")
logger.setLevel(logging.INFO)

def elapsed(func):
    def wrap(*args):
        start_r = time.perf_counter()
        start_p = time.process_time()
        ret = func(*args)
        end_r = time.perf_counter()
        end_p = time.process_time()
        elapsed_r = end_r - start_r
        elapsed_p = end_p - start_p

        logger.info(f'[{func.__name__}]\nelapsed: {elapsed_r:.6f}sec (real) / {elapsed_p:.6f}sec (cpu)')
        return ret
    return wrap