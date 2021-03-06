import time
import json
from tweepy import RateLimitError

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


def get_time() -> dict:
    timevar = time.localtime()
    hours = '0' + \
        str(timevar.tm_hour) if timevar.tm_hour < 10 else str(timevar.tm_hour)
    mins = '0' + \
        str(timevar.tm_min) if timevar.tm_min < 10 else str(timevar.tm_min)
    secs = '0' + \
        str(timevar.tm_sec) if timevar.tm_sec < 10 else str(timevar.tm_sec)

    return {
        'log_string': '[' + hours + ':' + mins + ':' + secs + '] ',
        'no_brackets_time': hours + ':' + mins + ':' + secs,
        'month_int': timevar.tm_mon,
        'day_int': timevar.tm_mday
    }


def append_json(file_name: str, mapa):
    try:
        with open(file_name, 'r') as f:
            f_obj = json.load(f)
    except FileNotFoundError:
        print(
            f'{get_time()["log_string"]}Nie znaleziono pliku o nazwie {file_name}')
        return

    if type(mapa) == list:
        f_obj = f_obj + mapa
    elif type(mapa) == dict:
        f_obj = f_obj | mapa
    
    with open(file_name, 'w') as f:
        json.dump(f_obj, f)


# def print_log(*args):
#    print(get_time()['log_string'], end="")
#    print(*args)
# TODO

def log(arg: str):
    if len(arg) <= 30:
        log = 'Odpowiedziano na tweet\'a o tresci: '+arg
    else:
        buff = str()
        for c in arg[30:]:
            if c == ' ':
                break
            buff = buff + c
        log = 'Odpowiedziano na tweet\'a o tresci: ' + \
            arg[:30]+buff+'...'
    print(get_time()['log_string']+log)

    log_map = [{
        'month': get_time()['month_int'],
        'day': get_time()['day_int'],
        'time': get_time()['no_brackets_time'],
        'log': log
    }]
    append_json('logi.json', log_map)


def handle_error(error: BaseException):
    if error == RateLimitError:
        error_msg = f'{get_time()["log_string"]}Rate limited'
        print(error_msg)

        log_map = [{
            'month': get_time()['month_int'],
            'day': get_time()['day_int'],
            'time': get_time()['no_brackets_time'],
            'log': "ERROR: Rate limited"
        }]
        append_json('logi.json', log_map)

        time.sleep(900)
        return

    error_msg = f'{get_time()["log_string"]}Błąd'
    print(error_msg)

    log_map = [{
        'month': get_time()['month_int'],
        'day': get_time()['day_int'],
        'time': get_time()['no_brackets_time'],
        'log': "ERROR: "+str(error)
    }]
    append_json('logi.json', log_map)


if __name__ == '__main__':
    # TODO: GRAPH
    pass
