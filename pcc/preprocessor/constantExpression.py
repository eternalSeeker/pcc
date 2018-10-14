
from enum import Enum


class logic(Enum):
    OR = 1
    AND = 2
    XOR = 3


class constantExpression:

    @staticmethod
    def assertEqual(a, b):
        if isinstance(a, str):
            assert a == b, '<%s> != <%s>' % (a, b)
        else:
            assert a == b, '<%s> != <%s>' % (str(a), str(b))

    def __init__(self, constantExpressionString):
        self.constantExpressionString = constantExpressionString

    def evaluate(self):
        result = False
        string = self.constantExpressionString.strip()

        list_of_elements = []
        element = ''
        i = 0
        while i < len(string):
            if string[i] == '|' and 1+1 < len(string) and string[i+1] == '|':
                list_of_elements.append(element)
                list_of_elements.append(logic.OR)
                i += 2
                element = ''
            elif string[i] == '&' and 1+1 < len(string) and string[i+1] == '&':
                list_of_elements.append(element)
                list_of_elements.append(logic.AND)
                i += 2
                element = ''
            else:
                element += string[i]
                i += 1
        # add the last parsed element to the list
        list_of_elements.append(element)
        i = 0
        while i < len(list_of_elements):
            # check if the eval is something like '1' or '0'
            stripped_string = list_of_elements[i].strip()
            if stripped_string.isdigit():
                number = int(stripped_string)
                result = number != 0
            i += 1

        return result
