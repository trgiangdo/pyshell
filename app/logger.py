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
    def dump(cls, output_path: Optional[str]):
        if output_path:
            f = open(output_path, "w")

        for msg in cls.__log:
            if msg[0] == "info":
                if output_path:
                    f.write(msg[2] + "\n")
                    continue

            print(msg[2])

        if output_path:
            f.close()
        cls.__log.clear()
