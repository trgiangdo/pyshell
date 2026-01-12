import datetime
from typing import List, Optional, Tuple


class Logger:
    __log: List[Tuple[str, datetime.datetime, str]] = []

    @classmethod
    def info(cls, message: str):
        cls.__log.append(("info", datetime.datetime.now(), message))

    @classmethod
    def error(cls, message: str):
        cls.__log.append(("error", datetime.datetime.now(), message))

    @classmethod
    def dump(cls, info_path: Optional[str], error_path: Optional[str]):
        if info_path:
            info_f = open(info_path, "w")
        if error_path:
            error_f = open(error_path, "w")

        for msg in cls.__log:
            if msg[0] == "info":
                if info_path:
                    info_f.write(msg[2] + "\n")
                    continue

            if msg[0] == "error":
                if error_path:
                    error_f.write(msg[2] + "\n")
                    continue

            print(msg[2])

        if info_path:
            info_f.close()
        if error_path:
            error_f.close()
        cls.__log.clear()
