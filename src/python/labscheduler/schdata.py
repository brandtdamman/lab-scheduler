# Placeholder comment/docstring

class Ta:
    def __init__(self, name: str, identifier: int):
        self._name = name
        self._id = identifier

    def __repr__(self):
        return self._id

    def __str__(self):
        return self._name

class Lab:
    def __init__(self, identifier: int, start_time: float,
                    end_time: float, max_tas: int):
        self._id = identifier

        self._start = start_time
        self._start_str = self._converttime(self._start)
        self._end = end_time
        self._end_str = self._converttime(self._end)
        self._maxLen = max_tas

        self.cleartas()

    def _converttime(self, input_time: float) -> str:
        #? TODO: Move to support module?
        floating_time = 0
        if isinstance(input_time, float):
            floating_time = round((input_time - int(input_time)) * 100)

        input_time = int(input_time)
        if input_time > 12:
            input_time = input_time - 12
        
        output = f"{input_time}:{floating_time:02}"
        return output

    def addta(self, assistant: Ta):
        if len(self._tas) == self._maxLen:
            raise ValueError("Cannot add another teaching assistant to lab.")
        self._tas.append(assistant)

    def removeta(self, assistant):
        # Need to find out how to overload...?
        if len(self._tas) == 0:
            raise ValueError("Cannot remove from empty teaching assistants list.")
        # TODO: Return the removed assistant

    def cleartas(self):
        self._tas = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Lab Section {self._id} at {self._start_str}-{self._end_str}'

class Schedule:
    def __init__(self):
        self._week: dict = {}
        
        # Setup the workweek
        self._week['Monday'] = []
        self._week['Tuesday'] = []
        self._week['Wednesday'] = []
        self._week['Thursday'] = []
        self._week['Friday'] = []

    def _matchDay(self, val: str) -> bool:
        for key in self._week:
            if key == val:
                return True
        return False

    def addsection(self, section: Lab, day: str):
        if not self._matchDay(day):
            raise ValueError("Invalid week day.")
        self._week[day].append(section)
