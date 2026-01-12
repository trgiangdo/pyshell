import os
from typing import Any, Callable, Dict, List
from pathlib import Path

from .logger import Logger
from .utils import find_executable


def handle_exit(args: List[str]):
    exit()


def handle_echo(args: List[str]):
    Logger.info(" ".join(args[1:]))


def handle_type(args: List[str]):
    message = args[1]
    if message.strip() in builtin_command:
        Logger.info(f"{message} is a shell builtin")
        return

    if exec_path := find_executable(message):
        Logger.info((f"{message} is {exec_path}"))
        return

    Logger.error(f"{message}: not found")


def handle_pwd(args: List[str]):
    Logger.info(os.getcwd())


def handle_cd(args: List[str]):
    des = args[1]
    des = des.replace("~", str(Path.home()), 1)

    if not os.path.exists(des):
        Logger.error(f"cd: {des}: No such file or directory")
        return

    os.chdir(des)


builtin_command: Dict[str, Callable[[List[str]], Any]] = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "pwd": handle_pwd,
    "cd": handle_cd,
}
