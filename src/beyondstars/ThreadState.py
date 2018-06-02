# -*-coding:UTF-8 -*
from enum import Enum


class ThreadState(Enum):
	INITIALIZING = 0
	STARTED = 1
	PAUSED = 2
	STOPPED = 3
