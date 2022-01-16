# placeholder comment/docstring
from schdata import Serialized

def rtd_dict(root: dict) -> dict:
    placeholder = dict()
    for key in root:
        element = root[key]
        if isinstance(element, dict):
            placeholder[key] = rtd_dict(element)
        elif isinstance(element, list):
            placeholder[key] = rtd_list(element)
        elif issubclass(element.__class__, Serialized):
            placeholder[key] = element.todict()
        else:
            placeholder[key] = element

    return placeholder

def rtd_list(root: list) -> list:
    placeholder = list()
    for element in root:
        if isinstance(element, dict):
            placeholder.append(rtd_dict(element))
        elif isinstance(element, list):
            placeholder.append(rtd_list(element))
        elif issubclass(element.__class__, Serialized):
            placeholder.append(element.todict())
        else:
            placeholder.append(element)

    return placeholder

_WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
def match_day(val: str) -> bool:
    for day in _WEEKDAYS:
        if day == val or day[0] == val.upper():
            return True
    return False

def isfloating(val: str) -> bool:
    try:
        float(val)
        return True
    except ValueError:
        return False

def isjson(filename: str) -> bool:
    period = filename.rfind('.')
    if period == -1:
        return False
    if filename[period:] != 'json':
        return False
    return True

def sl_input(lines_to_clear: int) -> str:
    # Perform same line input.
    val = input()
    print('\033[{}C\033[{}A'.format(len(val) + 4,\
        lines_to_clear), end='\r')
    return val


from typing import Callable
def slc_input(lines_to_clear: int,
            conditional: Callable[[str], bool]) -> (str, bool):
    val = input()
    result = conditional(val)
    if not result:
        print('\033[{}C\033[{}A'.format(len(val) + 4,\
            lines_to_clear), end='\r')
    
    return (val, result)

def r_input(msg: str, err_msg: str, input_msg: str, 
            rtype: type, conditional: Callable[[str], bool]) -> str:
    if msg:
        print(msg)

    failed_once: bool = False
    clear_lines: int = 1
    while True:
        if failed_once:
            clear_lines = 2
        
        print(input_msg, end='')
        user_input, is_valid = slc_input(clear_lines, conditional)
        if is_valid:
            return rtype(user_input)

        print(f'Invalid input ({user_input}). {err_msg}')
        failed_once = True
