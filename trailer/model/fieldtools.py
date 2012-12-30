from datetime import datetime
import dateutil.parser

def make(t):
    return lambda items: t(items) if items is not None else t()

make_list = make(list)


def make_time(time):
    return time if isinstance(time, datetime) else dateutil.parser.parse(time)



def nullable(t):
    return lambda x: t(x) if x is not None else None




def attempt(f, default=None, exception=(ValueError, TypeError)):

    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if isinstance(e, exception):
                return default
            raise

    return func