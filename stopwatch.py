from datetime import datetime, timedelta


class stopwatch:

    __isRunning = False
    
    __history : list

    __start_time = datetime.now()
    __stop_time = __start_time
    __offset = timedelta()

    @property
    def isRunning(self) -> bool: 
        return self.__isRunning

    @property
    def time(self) -> timedelta:
        offset = timedelta()
        now = datetime.now()
        if not self.__isRunning: offset += now - self.__stop_time
        return now - self.__start_time - (offset + self.__offset)

    @property
    def history(self) -> list:
        return self.__history.copy()

    def __init__(self, stopped = True) -> None:
        self.reset()
        if not stopped: self.start()

    def start(self) -> None:
        if self.__isRunning: return
        self.__offset += datetime.now() - self.__stop_time
        self.__stop_time = None
        self.__isRunning = True

    def stop(self) -> None:
        if not self.__isRunning: return
        self.__stop_time = datetime.now()
        self.__isRunning = False

    def reset(self) -> None:
        self.__history = []
        self.__start_time = datetime.now()
        self.__stop_time = self.__start_time
        self.__offset = timedelta()

    def split(self) -> None:
        self.__history.append(self.time)
