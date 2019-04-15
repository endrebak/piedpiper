import inspect
import sys


def _leading_spaces(l):
    return len(l) - len(l.lstrip(' '))


def _get_lines_in_block(filename, line_nb):

    lines = []
    with open(filename) as f:
        for _ in range(line_nb):
            next(f)

        line = f.readline()
        while line.strip().startswith("#"):
            line = f.readline()

        first_line = line
        first_leading_spaces = _leading_spaces(first_line)
        lines.append(first_line)

        for line in f:
            if line.strip().startswith("#"):
                continue
            if _leading_spaces(line) >= first_leading_spaces:
                lines.append(line)
            else:
                break

    return lines


def _parse_commands(code):

    # parsing top-level commands
    level = 0
    starts = []
    dot_without_paren = False
    open_call = False
    lastchar = None
    for i, char in enumerate(code, 0):
        if char in (" ", "\n", "\t"): continue

        if char == "(":
            if lastchar == ")" and level == 0:
                starts.append((i, char))
                open_call = True
            dot_without_paren = False
            level += 1
        elif char == ")":
            if open_call and level == 0:
                open_call = False
            level -= 1
        elif level == 0 and char == "." and not dot_without_paren:
            dot_without_paren = True
            starts.append((i, char))
        lastchar = char

    commands = []
    last_i = None
    for (i, _) in starts:
        commands.append(code[last_i:i])
        last_i = i
    commands.append(code[last_i:])

    return commands


def _fix_square_brackets(commands):

    new_commands = []
    for command in commands:
        # print(command)
        # helplen = (int(len(command) / 10) + 1)
        # for i in range(0, helplen):
        #     print(str(i) * 10, end="")

        # print("")
        # print("1234567890" * helplen)

        paren_level = 0
        bracket_level = 0
        starts = []
        for i, char in enumerate(command):
            if char == "(":
                paren_level += 1
            elif char == ")":
                paren_level -= 1
            elif paren_level == 0 and char == "[":  # start
                if bracket_level == 0:
                    starts.append(i)
                bracket_level += 1
            elif char == "]" and bracket_level != 0:
                bracket_level -= 1
                if bracket_level == 0 and paren_level == 0:
                    starts.append(i + 1)

        last_i = None
        for i in starts:
            new_command = command[last_i:i]
            if new_command:
                new_commands.append(new_command)
            last_i = i
        new_commands.append(command[last_i:])

    return new_commands


def _run_commands(commands, start_line, source_file, _locals):

    locals().update(_locals)
    clean = " ".join(commands[0].split()).strip()
    if "=" in clean:
        clean = clean.split("=")[1]
    var_name = "__dbg"
    __dbg = eval(clean)
    print("Start data:", file=sys.stderr)
    print(__dbg, file=sys.stderr)
    print("", file=sys.stderr)

    for command in commands[1:]:
        clean = " ".join(command.split()).strip().\
            replace("( ", "(").replace(") ", ")")
        if not clean:
            continue  # TODO: find out why some are empty
        print("{}\n".format(clean), file=sys.stderr)
        dirty = var_name + clean
        __dbg = eval(dirty)
        print(__dbg, file=sys.stderr)
        print("", file=sys.stderr)

    print("[{}:{}]".format(source_file, start_line), file=sys.stderr)


# def _find_var_name()


class Debug:
    def __init__(self, _locals=None):
        if _locals is None:
            _locals = {}
        frames = inspect.stack()

        for frame in frames:
            line = frame.code_context[0]
            if "Debug" in line:
                # self.filename = frame.filename
                # self.lineno = frame.lineno
                break

        lines = _get_lines_in_block(frame.filename, frame.lineno)

        code = "".join(lines)

        commands = _parse_commands(code)

        brackets_fixed = _fix_square_brackets(commands)

        _run_commands(brackets_fixed, frame.lineno, frame.filename, _locals)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
