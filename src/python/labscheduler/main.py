""" Main thread for Lab Scheduler.  Handles basic input
    and related tasks not suited for specialized files.

    :author: Daryl Damman
    :since: 03-January-2022
"""
from schdata import *

def semesterschedule():
    import os
    os.system('cls')

    print(' CREATING SEMESTER SCHEDULE\n' + '=' * 28, end='\n\n')
    # print(len('CREATING SEMESTER SCHEDULE'))

    # Determine how many TAs may be added to any given section
    print('Maximum number of TAs per lab? >>', end=' ')
    max_tas = input()

    # Avoid invalid inputs, replace if needed
    if not max_tas.isnumeric():
        print(f'Invalid input ({max_tas}), using maximum of 2 TAs per lab')
        max_tas = 2

    current_schedule = Schedule()

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

        while True:
            print(' >>', end=' ')
            start_time = input()
            if not _isfloating(start_time):
                print(f'Invalid time ({start_time}) inputted. Try again.')
                continue
            else:
                start_time = float(start_time)
                break

        print('When does this section end (same format as start)?')
        while True:
            print(' >>', end=' ')
            end_time = input()
            if not _isfloating(end_time):
                print(f'Invalid time ({end_time}) inputted. Try again.')
                continue
            else:
                end_time = float(end_time)
                break
        
        current_section = Lab(section_number, start_time, end_time, max_tas)
        print('Lab section made.\nWhat day is this secion held?')

        while True:
            print(' >>', end=' ')
            day = input()
            try:
                current_schedule.addsection(current_section, day)
                break
            except ValueError as e:
                print(str(e))

        print(f'Lab section {section_number} added to schedule')

    for day in current_schedule._week:
        print(day, current_schedule._week[day])

def _isfloating(val: str) -> bool:
    try:
        float(val)
        return True
    except ValueError:
        return False

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