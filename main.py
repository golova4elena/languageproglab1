import json
import pytz
import tzlocal
import paste.httpserver
import pandas
import datetime

def do_get(data):
    answer = "\tTime is "
    if not data:
        data = None
    else:
        try:
            data = pytz.timezone(data)
        except pytz.UnknownTimeZoneError:
            answer = '\tError in time zone'
            return answer
    answer += datetime.datetime.now(tz = data).time().isoformat()
    return answer

def do_post(data):
    if not isjson(data):
        answer = 'Error in json format'
        return answer
    else:
        data = json.loads(data)
        if(data['type'] == 'time'):
            answer = post_time(data)
        elif(data['type'] == 'date'):
            answer = post_date(data)
        elif (data['type'] == 'datediff'):
            answer = post_datediff(data)
        return answer

def isjson(data):
    answer = True
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        answer = False
    return answer

def post_time(data):
    try:
        tz = pytz.timezone(data['tz'])
    except KeyError:
        tz = None
    if not tz:
        tz = tzlocal.get_localzone()
    return json.dumps({'tz': str(tz), 'time': datetime.datetime.now(tz = tz).time().isoformat()})

def post_date(data):
    try:
        tz = pytz.timezone(data['tz'])
    except KeyError:
        tz = None
    if not tz:
        tz = tzlocal.get_localzone()
    return json.dumps({'tz': str(tz), 'date': datetime.datetime.now(tz = tz).date().isoformat()})

def post_datediff(data):
    try:
        first_tz = pytz.timezone(data['start'])
    except KeyError:
        first_tz = None
    if not first_tz:
        first_tz = tzlocal.get_localzone()
    try:
        second_tz = pytz.timezone(data['end'])
    except KeyError:
        second_tz = None
    if not second_tz:
        second_tz = tzlocal.get_localzone()
    date = pandas.to_datetime(datetime.datetime.now(tz = first_tz).date().isoformat())
    if first_tz.localize(date) >= second_tz.localize(date):
        delta = (first_tz.localize(date) - second_tz.localize(date).astimezone(first_tz)).seconds/3600
    else:
        delta = -(24 - ((first_tz.localize(date) - second_tz.localize(date).astimezone(first_tz)).seconds / 3600))
    return json.dumps({'datediff': delta, 'start': str(first_tz), 'end': str(second_tz)})

def run_server(env, start_response):
    if env['REQUEST_METHOD'] == 'GET':
        data = env['PATH_INFO'][1:]
        answer = do_get(data)
    if env['REQUEST_METHOD'] == 'POST':
        data = env['wsgi.input']
        answer = do_post(data.read().decode("utf-8"))
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [bytes(answer, encoding='utf-8')]

paste.httpserver.serve(run_server)
