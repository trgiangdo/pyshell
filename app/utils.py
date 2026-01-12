import os
from typing import List


def find_executable(command: str) -> str:
    PATH = os.environ["PATH"]
    for path in PATH.split(os.pathsep):
        if not os.path.exists(path):
            continue

        file_path = os.path.join(path, command)
        if os.access(file_path, os.X_OK):
            return file_path

    return ""


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


def redirect_output(args: List[str]):
    info_path = None
    error_path = None
    dump_mode = "w"
    if len(args) > 2 and args[-2] in [">", "1>", "2>", "1>>", ">>", "2>>"]:
        if args[-2] in [">", "1>", "1>>", ">>"]:
            info_path = args[-1]
        elif args[-2] in ["2>", "2>>"]:
            error_path = args[-1]

        if args[-2].endswith(">>"):
            dump_mode = "a"

        args = args[:-2]

    return args, info_path, error_path, dump_mode
