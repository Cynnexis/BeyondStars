import time


class Time(object):
	get_current_millis = lambda: time.time() * 1000
