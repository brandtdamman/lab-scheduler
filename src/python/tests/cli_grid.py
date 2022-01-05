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
        # print(ta)
        ta_ids[ta_names[ta][2]] = ta

    # print(ta_ids)

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
    #? The magical 3 is for Lab section #, time, and buffer space
    #?      Need to ensure _some_ value for maxTaPerLab is set.
    # TODO  Probably do a preemptive scan and see the largest TA
    #       \-> gathering rather than a preset magick number.
    row_height = ta_schedule.get('maxTaPerLab', 2) + 3
    # print(row_height)

    """

    Example time chunk.
    Solution: Do not conform to a grid for now.

    |-------------|
    | Section 4   |
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

    #! Debug value to compare adding spacing buffer before
    #!      or after the TA substring.
    _AFTER = False

    daily_labsections = {}
    for day in ta_schedule['schedule']:
        # Setup the day's lab sections, linearly
        today = day['day'] #? Mildly confusing, change later?

        # If for some weird reason there are duplicate days,
        #   go ahead and simply append to the bottom...?
        if not daily_labsections.get(today, None):
            daily_labsections[today] = []

            # Print the header
            header = ("| {:" + str(column_length - 1) + "}|").format(today)
            header = header + "\n|" + ("-" * column_length) + "|"
            daily_labsections[today].append((header.split('\n'), 0))

        # Sort by section start time and print respectively
        day['labs'].sort(key=sortingFunc)

        # TODO: Move elsewhere...
        def formatTime(input_time: float) -> str:
            """Converts a floating point time into string format
            using standard formatting (hh:mm) with no regard to
            AM versus PM.

            :param input_time: floating-point time value from json schedule
            :type input_time: float
            :return: finalized output string
            :rtype: str
            """
            floating_time = 0
            if isinstance(input_time, float):
                floating_time = round((input_time - int(input_time)) * 100)

            input_time = int(input_time)
            if input_time > 12:
                input_time = input_time - 12
            
            output = f"{input_time}:{floating_time:02}"
            return output

        # Add each respective lab section into the "grid list"
        for lab in day['labs']:
            row_counter = 3
            current_section = ("| {:" + str(column_length - 1) + "}|").format(f"Section {lab['id']}")

            # Convert times in schedule to real times
            start_time = formatTime(lab['startTime'])
            end_time = formatTime(lab['endTime'])

            # TODO: Nested string formatting.  Needs improvement.
            # Needs to stay on one line or broken into chunks.
            current_section = f'{current_section}\n{("| {:" + str(column_length - 1) + "}|").format(f"{start_time}-{end_time}")}'

            # Add buffer from section number and time slot
            current_section = current_section + ("\n|" + (" " * column_length) + "|")

            # Add respective TAs to the listing
            ta_substring = ''
            for ta in lab['tas']:
                ta_substring = ta_substring + ("\n| {:" + str(column_length - 1) + "}|").format(ta_ids[ta['id']])
                row_counter = row_counter + 1

            if not _AFTER:
                # Append TA substring to current section string
                current_section = current_section + ta_substring
            
            # If the current section is too short, add buffers.
            if row_counter < row_height:
                for x in range(row_height - row_counter):
                    current_section = current_section + ("\n|" + (" " * column_length) + "|")

            if _AFTER:
                # Append TA substring to current section string
                current_section = current_section + ta_substring

            #? Consider removing this during the print-out process
            current_section = current_section + "\n|" + ("-" * column_length) + "|"

            daily_labsections[today].append((current_section.split('\n'), lab['startTime']))

    # 5. Find longest day, add filler spaces based on time slots
    #?  \-> Sort by hours.  Won't line up perfectly but it will be close enough.
    # for section in daily_labsections['Thursday']:
    #     for element in section:
    #         print(element, end='')
    #     print()
    # longest_day = None
    # for day in daily_labsections:
    #     if not longest_day or longest_day[1] < len(daily_labsections[day]):
    #         longest_day = (day, len(daily_labsections[day]))

    # print(f"{longest_day[0]} is the longest day with {longest_day[1] - 1} sections.")
    def weeklyOrder(e):
        if e[1] == "Monday":
            return 0
        elif e[1] == "Tuesday":
            return 1
        elif e[1] == "Wednesday":
            return 2
        elif e[1] == "Thursday":
            return 3
        elif e[1] == "Friday":
            return 4
        else:
            return 100

    tuple_schedule = []
    def tupleScheduleSorting(e):
        return e[1]

    for day in daily_labsections:
        daily_labsections[day].sort(key=tupleScheduleSorting)
        tuple_schedule.append((daily_labsections[day], day))

    tuple_schedule.sort(key=weeklyOrder)
    # for day in tuple_schedule:
    #     for section in day[0]:
    #         print(section, end='')
    #     print()

    longest_day = (0, len(tuple_schedule[0][0]))
    for i in range(1, len(tuple_schedule)):
        if longest_day[1] < len(tuple_schedule[i][0]):
            longest_day = (i, len(tuple_schedule[i][0]))

    # Print the headers
    for i in range(2):
        output = ''
        for day in tuple_schedule:
            output = output + day[0][0][0][i]
        print(output)

    # Now the sections!
    fonce = True
    section_counters = {}
    for day in tuple_schedule:
        section_counters[day[1]] = 1

    def weeklyNumbers(e):
        if e == -1:
            return "Monday"
        elif e == 0:
            return "Tuesday"
        elif e == 1:
            return "Wednesday"
        elif e == 2:
            return "Thursday"
        else:
            return "Friday"
        
    # print(longest_day[0])
    for section in tuple_schedule[longest_day[0]][0]:
        if fonce:
            fonce = False
            continue
        # Determine if there should be fill-ins for
        #   certain sections
        needSpot = []
        for day in tuple_schedule:
            if len(day[0]) <= section_counters[day[1]]:
                needSpot.append(100)
            else:
                needSpot.append(round(day[0][section_counters[day[1]]][1]))

        # print(needSpot)
        smallest_value = 100
        for value in needSpot:
            if smallest_value > value:
                smallest_value = value

        # print(("|" + ("-" * column_length) + "|") * len(tuple_schedule))
        for i in range(row_height):
            day_counter = 0
            output = ''
            for result in needSpot:
                # print(tuple_schedule[day_counter][0][section_counter])
                if result == smallest_value or section_counters[tuple_schedule[longest_day[0]][1]] == longest_day[1] - 1 and result != 100:
                    output = output + tuple_schedule[day_counter][0][section_counters[weeklyNumbers(day_counter)]][0][i]
                else:
                    output = output + "|" + (" " * column_length) + "|"
                day_counter = day_counter + 1
            print(output)
        
        # section_counter = section_counter + 1
        count = 0
        for day in section_counters:
            # print(day)
            if needSpot[count] == smallest_value:
                section_counters[day] = section_counters[day] + 1
            count = count + 1
        
        print(("|" + ("-" * column_length) + "|") * len(tuple_schedule))

