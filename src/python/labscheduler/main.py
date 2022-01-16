""" Main thread for Lab Scheduler.  Handles basic input
    and related tasks not suited for specialized files.

    :author: Daryl Damman
    :since: 03-January-2022
"""
from typing import Optional

from schdata import *

def semesterschedule():
    import os
    os.system('cls')

    print(' CREATING SEMESTER SCHEDULE\n' + '=' * 28, end='\n\n')

    # Determine how many TAs may be added to any given section
    print('Maximum number of TAs per lab? >>', end=' ')
    max_tas = input()

    # Avoid invalid inputs, replace if needed
    if not max_tas.isnumeric():
        print(f'Invalid input ({max_tas}), using maximum of 2 TAs per lab')
        max_tas = 2

    current_schedule = Schedule(max_tas)

    import _support

    # Begin lab loop.
    while True:
        print('Enter a lab section number (or -1 to finish)')
        section_number = input()

        if section_number == "-1":
            break
        
        print('When does this section start?')
        print('Example inputs (use 24-hour format):')
        print('\t 8    --> 8:00 AM')
        print('\t 9.55 --> 9:55 AM')
        print('\t14.25 --> 2:25 PM')

        start_time = _support.r_input(None, "", ' >> ', float, _support.isfloating)
        # while True:
        #     print(' >>', end=' ')
        #     start_time = input()
        #     if not isfloating(start_time):
        #         print(f'Invalid time ({start_time}) inputted. Try again.')
        #         continue
        #     else:
        #         start_time = float(start_time)
        #         break

        print('When does this section end (same format as start)?')
        end_time = _support.r_input(None, "", ' >> ', float, _support.isfloating)
        # while True:
        #     print(' >>', end=' ')
        #     end_time = input()
        #     if not isfloating(end_time):
        #         print(f'Invalid time ({end_time}) inputted. Try again.')
        #         continue
        #     else:
        #         end_time = float(end_time)
        #         break
        
        current_section = Lab(section_number, start_time, end_time, max_tas)
        print('Lab section made.\nWhat day is this secion held?')

        day = _support.r_input(None, "Please enter M, T, W, R, or F (weekday)", ' >> ', str, _support.match_day)
        # while True:
        #     print(' >>', end=' ')
        #     day = input()
        #     try:
        #         current_schedule.addsection(current_section, day)
        #         break
        #     except ValueError as e:
        #         print(str(e))

        current_schedule.addsection(current_section, day)
        print(f'Lab section {section_number} added to schedule')

    # Temporary function for sorting day-to-day schedule.
    def labSorting(e: Lab):
        return e.start_time

    for day in current_schedule.week:
        # Sort, then print.
        current_schedule.week[day].sort(key=labSorting)
        print(day, current_schedule.week[day])

    # continue to next part of the scheduler
    createtas(current_schedule=current_schedule)

def createtas(current_schedule: Optional[Schedule] = None) -> None:
    """Requests a file for all TAs teaching the course or allows
    user to manually enter each TA individually in the console.

    All TAs must have a seniority rank, top 3 preferences, ID,
    and full name.

    :param current_schedule: schedule if already in-progress, defaults to None
    :type current_schedule: Schedule, optional
    """
    from _support import r_input, isjson
    import os

    #! TODO: Call _support function to change which screen clear is
    #   \-> called.
    os.system('cls')

    if not current_schedule:
        # Need to import schedule since there isn't one yet.
        filename = r_input('Enter filename of schedule (must be .JSON filetype).',\
            'Must be of form <NAME>.json', ' >> ', str, isjson)
        from fileio import jsontoschedule
        current_schedule = jsontoschedule(filename)

    def yn_input(val: str) -> bool:
        val = val.lower()
        if val == 'y' or val == 'yes' or val == '':
            return True
        return False

    resp = r_input('Do you wish to provide a JSON file of TAs?',\
        "This shouldn't happen.", ' >> ', str, yn_input)
    
    resp = yn_input(resp)
    if resp:
        # grab from file
        filename = r_input('Enter the filename for TA list.',\
            'Must be of form <NAME>.json', ' >> ', str, isjson)
        
        # TODO: Write fileio function to import JSON to TA list.
        pass

def assigntas(current_schedule: Optional[Schedule] = None) -> None:
    """Subroutine to automagically solve for one or more potential
    lab schedules where all TAs are assigned based on preference,
    seniority rank, and scheduling conflicts.

    :param current_schedule: schedule if already in-progress, defaults to None
    :type current_schedule: Schedule, optional
    """
    from _support import r_input
    import os

    #! TODO: Call _support function to change which screen clear is
    #   \-> called.
    os.system('cls')

    if not current_schedule:
        # Need to import schedule since there isn't one yet.
        def isjson(filename: str) -> bool:
            period = filename.rfind('.')
            if period == -1:
                return False
            
            if filename[period:] != 'json':
                return False

            return True
            
        filename = r_input('Enter filename of schedule (must be .JSON filetype).',\
            'Must be of form <NAME>.json', ' >> ', str, isjson)
        from fileio import jsontoschedule
        current_schedule = jsontoschedule(filename)

    from display import grid
    grid(current_schedule.todict())

    input()

def main():
    """ Entry point for Lab Scheduler application.
    """
    
    # Menu selection
    print('-' * 26 + '\n LAB SCHEDULER PROGRAM V1\n' + '-' * 26)
    while True:
        print('\n 1. Create semester schedule.')
        print(' 2. Add teaching assistants.')
        print(' 3. Solve for schedule(s).')
        #TODO: Add manual solve, not just automatic
        print(' 4. Exit program.')

        selection = ""
        while not selection.isnumeric():
            print('Select an option above >>', end=' ')
            selection = input()
            if not selection.isnumeric():
                print(f'Invalid option: {selection}.')

        if selection == "1":
            semesterschedule()
        else:
            break

if __name__=='__main__':
    main()