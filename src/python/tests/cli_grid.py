"""Given a test file, output appropriately.
"""

import json

if __name__=="__main__":
    json_lines = None

    while not json_lines:
        print(f"Enter test schedule filename: ")
        filename = input()

        try:
            with open(filename) as file:
                json_lines = file.readlines()
        except IOError:
            print(f"Warning: IO errors.  Check permissions and file existance.")

    # TODO: See if there is a better way of handling file read.
    json_string = ''
    for line in json_lines:
        json_string += line + '\n'

    ta_schedule = json.loads(json_string)

    # TODO: Serialize...?

    # print(ta_schedule)
    json_lines = None
    while not json_lines:
        print(f"Enter test TA list filename: ")
        filename = input()

        try:
            with open(filename) as file:
                json_lines = file.readlines()
        except IOError:
            print(f"Warning: IO errors.  Check permissions and file existance.")

    json_string = ''
    for line in json_lines:
        json_string += line + '\n'

    ta_list = json.loads(json_string)
    
    # 1. Collect names into new dictionary.
    ta_names = {}
    for ta in ta_list:
        # print(ta)
        space = ta['name'].index(' ')
        first_name = ta['name'][:space]

        # if len(first_name) < 3:
        #     # ! Bad fix for titles in name
        #     #FIXME
        #     second_space = ta['name'][space:].index(' ')
        #     if second_space != -1:
        #         first_name = ta['name'][space:second_space]

        if not ta_names.get(first_name, None):
            ta_names[first_name] = (ta['name'], space, ta['id'])
        elif ta_names[first_name] == True:
            # TODO: Avoid duplicate First Name, Last Initial.
            last_space = ta['name'].rfind(' ')
            full_name = f"{first_name} {ta['name'][last_space + 1]}."
            ta_names[full_name] = (ta['name'], space, ta['id'])
        else:
            other_name, __, other_id = ta_names[first_name]
            ta_names[first_name] = True

            #! TODO: DOES NOT ADD NEW TA TO DICTIONARY, ONLY UPDATES OLD.
            last_space = other_name.rfind(' ')
            full_name = f"{first_name} {other_name[last_space + 1]}."
            ta_names[full_name] = (ta['name'], space, other_id)

    # for ta in ta_names:
    #     print(ta)
    ta_ids = {}
    for ta in ta_names:
        if ta_names[ta] == True:
            continue
        print(ta)
        ta_ids[ta_names[ta][2]] = ta

    print(ta_ids)

    # 2. Find longest name.
    max_ta = None
    for ta in ta_names:
        if not max_ta or len(max_ta) < len(ta):
            max_ta = ta

    # print(max_ta)
    #? Filler section title that is the minimum width
    column_length = len(" 12:00-12:00 ")
    if column_length < len(max_ta):
        column_length = len(max_ta)

    # 3. Gather lab sections.
    # print(ta_schedule['schedule'])
    #? The magical 3 is for Lab section #, time, and buffer space
    row_height = ta_schedule.get('maxTaPerLab', 2) + 3

    """

    Example time chunk.
    Solution: Do not conform to a grid for now.

    |-------------|
    | Section  4  |
    | 8:00-9:55   |
    |             |
    | Daryl       |
    | Maxwell     |
    | Rayhanul    |
    |-------------|

    """

    # 4. Print schedule...?
    # TODO: Find a solution for overlapping labs.
    #   \-> There shouldn't be more than two-lab overlap... hopefully.
    #   \-> Potential idea: find overlapping labs, if any, and determine overlay amount.
    #       \_> From there, make the column length multiply by overlap.

    def sortingFunc(e):
        return e['startTime']

    for day in ta_schedule['schedule']:
        # Print the header
        print(("| {:" + str(column_length - 1) + "}|").format(day['day']))
        print("|" + ("-" * column_length) + "|")

        # Sort by section start time and print respectively
        day['labs'].sort(key=sortingFunc)

        # TODO: Move elsewhere...
        def formatTime(input_time):
            floating_time = 0
            if isinstance(input_time, float):
                floating_time = round((input_time - int(input_time)) * 100)

            input_time = int(input_time)
            if input_time > 12:
                input_time = input_time - 12
            
            output = f"{input_time}:{floating_time:02}"
            return output

        for lab in day['labs']:
            print(("| {:" + str(column_length - 1) + "}|").format(f"Section {lab['id']}"))

            # Convert times in schedule to real times
            start_time = formatTime(lab['startTime'])
            end_time = formatTime(lab['endTime'])

            print(("| {:" + str(column_length - 1) + "}|").format(f"{start_time}-{end_time}"))

            # Add respective TAs to the listing
            print("|" + (" " * column_length) + "|")
            for ta in lab['tas']:
                print(("| {:" + str(column_length - 1) + "}|").format(ta_ids[ta['id']]))

            print("|" + ("-" * column_length) + "|")

        # Clean up day
        print('\n')
