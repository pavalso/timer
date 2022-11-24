from datetime import timedelta
from time import sleep
from stopwatch import stopwatch
from wStopwatch import waiter


class timer(stopwatch):

    __targetTime : timedelta
    __waiter : waiter = None

    @property
    def time(self) -> timedelta:
        _time = super().time
        left = self.__targetTime - _time
        if left < timedelta(): left = timedelta()
        return left

    def __init__(self, targetTime : timedelta, stopped=True) -> None:
        self.__targetTime = targetTime
        self.__waiter = waiter(self.__targetTime.total_seconds() * 1000, self)
        super().__init__(stopped)

    def start(self) -> None:
        super().start()
        self.__waiter.run()

    def stop(self) -> None:
        super().stop()
        self.__waiter.stop()

    def wait(self) -> bool:
        return self.__waiter.wait()
