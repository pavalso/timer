from datetime import timedelta
from time import sleep
from threading import Thread, currentThread, Lock

from .stopwatch import stopwatch


class waiter:

    __forced : bool = False
    __wait : Thread = None

    __watch : stopwatch
    __targetTime : timedelta
    __lock : Lock

    def __init__(self, ms : int, watch : stopwatch = stopwatch(stopped = False)) -> None:
        self.__watch = watch
        self.__targetTime = self.__watch.time + timedelta(milliseconds=ms)
        self.__lock = Lock()
        self.__lock.acquire()
        if self.__watch.isRunning: self.run()

    def __tRun(self, ms : int) -> None:
        sleep(ms)
        if not currentThread() == self.__wait: return
        self.__lock.release()

    def run(self) -> None:
        if self.__wait: return
        ms = (self.__targetTime - self.__watch.time).total_seconds()
        self.__wait = Thread(target = self.__tRun, args = (ms,), daemon = True)
        self.__wait.start()

    def stop(self) -> None:
        self.__wait = None

    def terminate(self) -> None:
        self.__wait = None
        self.__forced = True
        self.__lock.release()

    def wait(self) -> bool:
        self.__lock.acquire()
        return not self.__forced

class wStopwatch(stopwatch):

    __waiters = []

    def start(self) -> None:
        for w in self.__waiters: w.run()
        return super().start()

    def stop(self) -> None:
        for w in self.__waiters: w.stop()
        return super().stop()

    def reset(self) -> None:
        for w in self.__waiters: w.terminate()
        return super().reset()

    def wait(self, ms : int) -> bool:
        w = waiter(ms, self)
        self.__waiters.append(w)
        ret = w.wait()
        self.__waiters.remove(w)
        return ret
