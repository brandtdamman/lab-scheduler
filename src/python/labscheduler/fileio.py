#placeholder comment/docstring

from typing import Optional
import json

def readable(filename: str) -> bool:
    """Conditional method to check if the given file (via filename)
    can be opened in this thread.

    :param filename: name of the file
    :type filename: str
    :return: true if file can be read, otherwise false
    :rtype: bool
    """
    try:
        handler = open(filename, 'r')

        # If the file is closed for some reason, we don't want to
        #   attempt reading it.
        result = handler.closed
        handler.close()
        return not result
    except IOError:
        #* File probably doesn't exist or not in given directory.
        return False

def j_open(filename: str) -> Optional[dict]:
    """Opens a JSON file and loads it into a dictionary.

    :param filename: name of file
    :type filename: str
    :return: JSON dictionary, or None if file could not be read
    :rtype: Optional[dict]
    """
    if not readable(filename):
        print('Error: Could not open desired JSON file.')
        #* Let the caller handle the unavailability.
        return None

    # Open and read contents.
    with open(filename, 'r') as file:
        json_file = file.read()

    # Return the dictionary.
    return json.loads(json_file)

def jp_open() -> Optional[dict]:
    #! TODO
    json_file = None

    # Continuously loops until user enters correct filename
    #   or manually closes program via KeyboardInterrupt
    while not json_file:
        print(f"Enter {fileInfo} filename: ")
        filename = input()

        # Attempt to open the file, otherwise print a warning message
        try:
            with open(filename) as file:
                json_file = file.read()
        except IOError:
            print(f"Warning: IO errors.  Check permissions and file existance.")

    # Deserialize and return dictionary
    return json.loads(json_file)

from schdata import Lab, Ta, Schedule
def jsontoschedule(filename: str) -> Schedule:
    """Creates a Schedule object from a JSON file.

    :param filename: name of JSON file
    :type filename: str
    :return: imported schedule based on JSON file
    :rtype: Schedule
    """
    file_dict = j_open(filename)
    
    # Make schedule object.
    current_schedule = Schedule(file_dict['max_tas'])

    # Create ta list.
    for ta_dict in file_dict['tas']:
        ta = Ta(ta_dict['name'], ta_dict['id'])
        current_schedule.tas.append(ta)

    # Add labs to import schedule.
    for day in file_dict['week']:
        # day is a key, not a dict
        for lab_dict in file_dict['week'][day]:
            lab = Lab(lab_dict['id'], lab_dict['start_time'],\
                lab_dict['end_time'], current_schedule.max_tas)
            current_schedule.addsection(lab, day)
    
    # Return imported schedule.
    return current_schedule