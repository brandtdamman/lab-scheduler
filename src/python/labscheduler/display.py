#placeholder comment/docstring

from fileio import j_open

def grid(schedule: dict) -> None:
    #! TODO: NEED TO VALIDATE DICTIONARY!!

    # 2. Find longest name, if any are present.
    max_ta = None
    for ta in schedule['tas']:
        if not max_ta or len(max_ta) < len(ta['name']):
            max_ta = ta['name']

    #? Filler section title that is the minimum width
    column_length = len(" 12:00-12:00 ")
    if max_ta and column_length < len(max_ta):
        column_length = len(max_ta)

    # 3. Gather lab sections.
    #? The magical 3 is for Lab section #, time, and buffer space
    #?      Need to ensure _some_ value for maxTaPerLab is set.
    # TODO  Probably do a preemptive scan and see the largest TA
    #       \-> gathering rather than a preset magick number.
    row_height = schedule.get('max_tas', 2) + 3

    # 4. Print schedule...?
    # TODO: Find a solution for overlapping labs.
    #   \-> There shouldn't be more than two-lab overlap... hopefully.
    #   \-> Potential idea: find overlapping labs, if any, and determine overlay amount.
    #       \_> From there, make the column length multiply by overlap.

    def sortingFunc(e):
        return e['start_time']

    #! Debug value to compare adding spacing buffer before
    #!      or after the TA substring.
    _AFTER = False

    daily_labsections = {}
    for day in schedule['week']:
        # Setup the day's lab sections, linearly
        today = schedule['week'][day]

        # If for some weird reason there are duplicate days,
        #   go ahead and simply append to the bottom...?
        if not daily_labsections.get(day, None):
            daily_labsections[day] = []

            # Print the header
            header = ("| {:" + str(column_length - 1) + "}|").format(day)
            header = header + "\n|" + ("-" * column_length) + "|"
            daily_labsections[day].append((header.split('\n'), 0))

        # Sort by section start time and print respectively
        today.sort(key=sortingFunc)

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
        for lab in today:
            row_counter = 3
            current_section = ("| {:" + str(column_length - 1) + "}|").format(f"Section {lab['id']}")

            # Convert times in schedule to real times
            start_time = formatTime(lab['start_time'])
            end_time = formatTime(lab['end_time'])

            # TODO: Nested string formatting.  Needs improvement.
            # Needs to stay on one line or broken into chunks.
            current_section = f'{current_section}\n{("| {:" + str(column_length - 1) + "}|").format(f"{start_time}-{end_time}")}'

            # Add buffer from section number and time slot
            current_section = current_section + ("\n|" + (" " * column_length) + "|")

            # Add respective TAs to the listing
            ta_substring = ''
            for ta in lab['tas']:
                ta_substring = ta_substring + ("\n| {:" + str(column_length - 1) + "}|").format(ta['name'])
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

            daily_labsections[day].append((current_section.split('\n'), lab['start_time']))

    # 5. Find longest day, add filler spaces based on time slots
    #?  \-> Sort by hours.  Won't line up perfectly but it will be close enough.
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
        if e == 0:
            return "Monday"
        elif e == 1:
            return "Tuesday"
        elif e == 2:
            return "Wednesday"
        elif e == 3:
            return "Thursday"
        else:
            return "Friday"
        
    while True:
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
        
        if smallest_value == 100:
            break

        # print(("|" + ("-" * column_length) + "|") * len(tuple_schedule))
        for i in range(row_height):
            day_counter = 0
            output = ''
            for result in needSpot:
                # print(tuple_schedule[day_counter][0][section_counter])
                if result == smallest_value:
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

if __name__=="__main__":
    file_input: dict = j_open("test_output.json")
    grid(file_input)