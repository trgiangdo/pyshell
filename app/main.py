import subprocess
import sys
import os
from typing import Any, Callable, Dict, List
from pathlib import Path
import itertools


def parse_args(user_command: str) -> List[str]:
    def parse_single_quote(command: str) -> List[str]:
        quote_split = command.replace("''", "").split("'")
        args = [quote_split[i].split(" ") if not i%2 else [quote_split[i]] for i in range(len(quote_split))]
        return [x for x in list(itertools.chain.from_iterable(args)) if x]

    def parse_double_quote(command: str) -> List[str]:
        quote_split = command.replace('""', "").split('"')
        args = [parse_single_quote(quote_split[i]) if not i%2 else [quote_split[i]] for i in range(len(quote_split))]
        return [x for x in list(itertools.chain.from_iterable(args)) if x]

    return parse_double_quote(user_command)


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
    print(" ".join(args[1:]))


def handle_type(args: List[str]):
    message = args[1]
    if message.strip() in builtin_command:
        print(f"{message} is a shell builtin")
        return

    if exec_path := find_executable(message):
        print((f"{message} is {exec_path}"))
        return

    print(f"{message}: not found")


def handle_pwd(args: List[str]):
    print(os.getcwd())


def handle_cd(args: List[str]):
    des = args[1]
    des = des.replace("~", str(Path.home()), 1)

    if not os.path.exists(des):
        print(f"cd: {des}: No such file or directory")
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

    for command, command_handler in builtin_command.items():
        if args[0] == command:
            command_handler(args)
            break
    else:
        if find_executable(args[0]):
            result = subprocess.run(args, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip())
        else:
            print(f"{args[0]}: command not found")


if __name__ == "__main__":
    while True:
        main()
