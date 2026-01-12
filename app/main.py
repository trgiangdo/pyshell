import subprocess
import sys
import os
from typing import Any, Callable, Dict, List
from pathlib import Path

from .logger import Logger


def parse_args(user_command: str) -> List[str]:
    args = []

    arg = ""
    single_quote = False
    double_quote = False
    backslash = False
    for current_char in user_command:
        if backslash:
            if double_quote and (current_char != "\\" and current_char != '"'):
                arg += "\\"
            arg += current_char
            backslash = False
        elif current_char == "\\" and not single_quote:
            backslash = True
        elif current_char == "'" and not double_quote:
            single_quote = not single_quote
        elif current_char == '"' and not single_quote:
            double_quote = not double_quote
        elif current_char == " " and not single_quote and not double_quote:
            if arg:
                args.append(arg)
                arg = ""
        else:
            arg += current_char

    if arg:
        args.append(arg)
    return args



def find_executable(command: str) -> str:
    PATH = os.environ["PATH"]
    for path in PATH.split(os.pathsep):
        if not os.path.exists(path):
            continue

        file_path = os.path.join(path, command)
        if os.access(file_path, os.X_OK):
            return file_path

    return ""


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


def main():
    sys.stdout.write("$ ")
    user_command = input()
    args = parse_args(user_command)

    info_path = None
    error_path = None
    if len(args) > 2 and args[-2] in [">", "1>"]:
        info_path = args[-1]
        args = args[:-2]
    elif len(args) > 2 and args[-2] == "2>":
        error_path = args[-1]
        args = args[:-2]


    for command, command_handler in builtin_command.items():
        if args[0] == command:
            command_handler(args)
            break
    else:
        if find_executable(args[0]):
            result = subprocess.run(args, capture_output=True, text=True)
            if result.stdout:
                Logger.info(result.stdout.strip())
            if result.stderr:
                Logger.error(result.stderr.strip())
        else:
            Logger.error(f"{args[0]}: command not found")

    Logger.dump(info_path, error_path)


if __name__ == "__main__":
    while True:
        main()
