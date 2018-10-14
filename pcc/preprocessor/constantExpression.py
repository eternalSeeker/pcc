
from enum import Enum, unique


@unique
class logic(Enum):

    def and_function(self, first_member):
        if first_member is False:
            return False
        else:
            return None

    def or_function(self, first_member):
        if first_member is True:
            return True
        else:
            return None

    OR = (1, or_function)
    AND = (2, and_function)
    XOR = (3, or_function)

    def __init__(self, enum_value, evaluate_function):
        self.enum_value = enum_value
        self.evaluate_function = evaluate_function

    def evaluate(self, first_member):
        return self.evaluate_function(self, first_member)


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

        list_of_elements = self.parse_input_string(string)

        i = 0
        while i < len(list_of_elements):
            element = list_of_elements[i]
            if isinstance(element, str):
                # check if the eval is something like '1' or '0'
                stripped_string = list_of_elements[i].strip()
                if stripped_string.isdigit():
                    number = int(stripped_string)
                    result = number != 0
            elif isinstance(element, logic):
                tmp = element.evaluate(result)
                if tmp:
                    return tmp
            i += 1

        return result

    def parse_input_string(self, string):
        list_of_elements = []
        element = ''
        i = 0
        while i < len(string):
            if string[i] == '|' \
                    and 1 + 1 < len(string) \
                    and string[i + 1] == '|':
                list_of_elements.append(element)
                list_of_elements.append(logic.OR)
                i += 2
                element = ''
            elif string[i] == '&' \
                    and 1 + 1 < len(string) \
                    and string[i + 1] == '&':
                list_of_elements.append(element)
                list_of_elements.append(logic.AND)
                i += 2
                element = ''
            else:
                element += string[i]
                i += 1
        # add the last parsed element to the list
        list_of_elements.append(element)
        return list_of_elements
