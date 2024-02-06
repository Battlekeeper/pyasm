new_line:str = "\\n"

class void:
    pass
def syscall(a: int = 0, b:int = 0) -> void:
    pass
def terminate() -> void:
    syscall(10)

def print_newline() -> void:
    global new_line
    syscall(4, new_line)

def print_int(number: int, new_line:int) -> void:
    syscall(1, number)
    if new_line == 1:
        print_newline()

def print_float(number: float, new_line:int) -> void:
    syscall(2, number)
    if new_line == 1:
        print_newline()
