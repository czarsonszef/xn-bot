import time

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


def get_time():
    timevar = time.localtime()

    hours = '0' + \
        str(timevar.tm_hour) if timevar.tm_hour < 10 else str(timevar.tm_hour)
    mins = '0' + \
        str(timevar.tm_min) if timevar.tm_min < 10 else str(timevar.tm_min)
    secs = '0' + \
        str(timevar.tm_sec) if timevar.tm_sec < 10 else str(timevar.tm_sec)

    return '[' + hours + ':' + mins + ':' + secs + '] '


def log_str(arg: str):
    if len(arg) <= 30:
        return get_time()+'Odpowiedziano na tweet\'a o tresci: '+arg

    buff = str()

    for c in arg[30:]:
        if c == ' ':
            break
        buff = buff + c

    log = get_time()+'Odpowiedziano na tweet\'a o tresci: '+arg[:30]+buff+'...'

    with open("logi.txt", "w") as f:
        f.write(log+'\n')

    return log
