# Placeholder comment/docstring

class Serialized:
    def __init__(self):
        pass

    def todict(self):
        from _support import rtd_dict, rtd_list
        output = {}
        for key in self.__dict__:
            if not key[0] == '_':
                element = self.__dict__[key]
                if isinstance(element, list):
                    output[key] = rtd_list(element)
                elif isinstance(element, dict):
                    output[key] = rtd_dict(element)
                elif issubclass(element.__class__, Serialized):
                    output[key] = element.todict()
                else:
                    output[key] = element

        return output

class Ta(Serialized):
    def __init__(self, name: str, identifier: int):
        self.name = name
        self.id = identifier

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return self.name

class Lab(Serialized):
    def __init__(self, identifier: int, start_time: float,
                    end_time: float, max_tas: int):
        self.id = identifier
        self.start_time = start_time
        self.end_time = end_time

        self._start_str = self._converttime(self.start_time)
        self._end_str = self._converttime(self.end_time)
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
        if len(self.tas) == self._maxLen:
            raise ValueError("Cannot add another teaching assistant to lab.")
        self.tas.append(assistant)

    def removeta(self, assistant):
        # Need to find out how to overload...?
        if len(self.tas) == 0:
            raise ValueError("Cannot remove from empty teaching assistants list.")
        # TODO: Return the removed assistant

    def cleartas(self):
        self.tas = []

    def __repr__(self):
        return f'#{self.id} @ {self._start_str}-{self._end_str}'

    def __str__(self):
        return f'Lab Section {self.id} at {self._start_str}-{self._end_str}'

class Schedule(Serialized):
    def __init__(self, max_tas: int):
        self.max_tas: int = max_tas
        self.tas: list = []
        self.week: dict = {}
        
        # Setup the workweek
        self.week['Monday'] = []
        self.week['Tuesday'] = []
        self.week['Wednesday'] = []
        self.week['Thursday'] = []
        self.week['Friday'] = []

    # def _matchDay(self, val: str) -> bool:
    #     for key in self.week:
    #         if key == val or key[0] == val.upper():
    #             return True
    #     return False

    def addsection(self, section: Lab, day: str):
        from _support import match_day
        if not match_day(day):
            raise ValueError("Invalid week day.")
        self.week[day].append(section)
