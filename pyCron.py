from croniter import *
from datetime import datetime
import time
import thread

_polls = {}

class BadCronError(CroniterBadCronError):
    '''.'''
class BadActionError(TypeError):
    '''.'''
class BadPollError(TypeError):
    '''.'''
class PollNameError(KeyError):
    '''.'''

class Poll:
    def __init__(self,crontab,action, action_args=None):
        try:
            self.croniter = croniter(crontab,datetime.now())
        except CroniterBadCronError as cron_err:
            raise BadCronError(cron_err)
        self.croniter.get_next()
        if callable(action):
            self.action = action
        else:
            raise BadActionError('['+str(action)+'] is not an exceptable action')
        self.action_args = action_args
class _Poll_Details:
    def __init__(self,name,poll):
        self.name=name
        self.cron_expr=" ".join(poll.croniter.exprs)
        self.action=poll.action.__name__
        self.action_args=poll.action_args

def add_poll(name,poll):
    if isinstance(poll, Poll):
        _polls[name] = poll
    else:
        raise BadPollError('['+str(poll)+'] is not type Poll')

def remove_poll(name):
    try:
        del _polls[name]
    except KeyError:
        raise PollNameError('['+str(name)+'] Poll, doesn\'t exist')

def get_polls_details():
    return [_Poll_Details(name,poll) for name,poll in _polls.copy().iteritems()]

def run_polls():
    for name, poll in _polls.copy().iteritems():
        if datetime.now().replace(second=0,microsecond=0) >= poll.croniter.get_current(datetime):
            print '['+str(datetime.now()) + '] Running `'+name+'`'
            if poll.action_args is None:
                poll.action(name=name,time=poll.croniter.get_current(datetime))
            else:
                poll.action(name=name,time=poll.croniter.get_current(datetime), **poll.action_args)
            poll.croniter.get_next()

def run_Cron():
    while True:
        run_polls()
        time.sleep(1)

#thread.start_new_thread(run_Cron,())
