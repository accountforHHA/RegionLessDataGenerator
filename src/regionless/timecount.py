import time
from functools import wraps

import cProfile
import pstats
import os

timebook = dict()


def timefn(fn):
    """计算性能的修饰器"""

    @wraps(fn)
    def measure_time(*args, **kwargs):
        DO_PROF = os.getenv("TIMING")
        global timebook
        if DO_PROF:
            t1 = time.time()
            result = fn(*args, **kwargs)
            t2 = time.time()
            if fn.__name__ not in timebook:
                timebook[fn.__name__] = t2 - t1
            else:
                timebook[fn.__name__] = timebook[fn.__name__] + t2 - t1
            #         print(f"@timefn: {timebook[fn.__name__]} took {t2 - t1: .5f} s")
            return result
        else:
            return fn(*args, **kwargs)

    return measure_time


def show():
    print(timebook)


# 性能分析装饰器定义
def do_cprofile(filename):
    """
    Decorator for function profiling.
    """

    def wrapper(func):

        def profiled_func(*args, **kwargs):
            # Flag for do profiling or not.
            DO_PROF = os.getenv("PROFILING")
            if DO_PROF:
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                # Sort stat by internal time.
                sortby = "tottime"
                ps = pstats.Stats(profile).sort_stats(sortby)
                ps.dump_stats(filename)
            else:
                result = func(*args, **kwargs)
            return result

        return profiled_func

    return wrapper
