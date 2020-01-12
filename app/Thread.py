import threading

class Thread(threading.Thread):
    def __init__(self, app, delay, func):
        super().__init__()
        self._kill = threading.Event()
        self._app = app
        self._delay = delay
        self._func = func

    def run(self):
        is_killed = self._kill.wait(self._delay)

        while not is_killed:
            self._func()
            is_killed = self._kill.wait(self._delay)
    
    def setDelay(self, delay):
        self._delay = delay

    def kill(self):
        self._kill.set()