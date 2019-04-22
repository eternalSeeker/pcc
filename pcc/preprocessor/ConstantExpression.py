
from enum import Enum, unique


def and_function(first_member):
    """Return False if the first member is False

    Args:
        first_member (bool): the first member of the and

    Returns:
        bool: False if the first argument is False, else None
    """
    if first_member is False:
        return False
    else:
        return None


def or_function(first_member):
    """Return True if the first member is True.

    Args:
        first_member (bool): the first member of the or

    Returns:
        bool: False if the first argument is True, else None
    """
    if first_member is True:
        return True
    else:
        return None


@unique
class Logic(Enum):

    OR = (1, or_function)
    AND = (2, and_function)
    XOR = (3, or_function)

    def __init__(self, enum_value, evaluate_function):
        """Create a logic object.

        Args:
            enum_value (int): A numeric identifier for the object
            evaluate_function : a function that takes 1 boolean argument and
                                returns a boolean or None
        """
        self.enum_value = enum_value
        self.evaluate_function = evaluate_function

    def evaluate(self, first_member):
        """Evaluate the expression

        Args:
            first_member (bool): The first part of the expression

        Returns:
            bool: if known else None
        """
        return self.evaluate_function(first_member)


class ConstantExpression:
    def __init__(self, constant_expression_string):
        """Create a constant expression.

        Args:
            constant_expression_string (str): The expression
        """
        self.constant_expression_string = constant_expression_string

    def evaluate(self):
        """Evaluate the constant expression.

        Returns:
            bool: The result of the constant expression
        """
        result = False
        string = self.constant_expression_string.strip()

        list_of_elements = self.parse_input_string(string)

        i = 0
        # loop over all elements in the list, and evaluate it
        while i < len(list_of_elements):
            element = list_of_elements[i]
            if isinstance(element, str):
                # check if the eval is something like '1' or '0'
                stripped_string = list_of_elements[i].strip()
                if stripped_string.isdigit():
                    number = int(stripped_string)
                    result = number != 0
            elif isinstance(element, Logic):
                tmp = element.evaluate(result)
                if tmp:
                    return tmp
            i += 1

        return result

    @staticmethod
    def parse_input_string(string):
        """Convert the string to a list of expressions to evaluate

        Args:
            string (str): The constant expression as a string

        Returns:
            list[str|Logic]: the list of elements to evaluate
        """
        list_of_elements = []
        element = ''
        i = 0
        while i < len(string):
            # is it ||
            if string[i] == '|' \
                    and 1 + 1 < len(string) \
                    and string[i + 1] == '|':
                list_of_elements.append(element)
                list_of_elements.append(Logic.OR)
                i += 2
                element = ''
            # is it &&
            elif string[i] == '&' \
                    and 1 + 1 < len(string) \
                    and string[i + 1] == '&':
                list_of_elements.append(element)
                list_of_elements.append(Logic.AND)
                i += 2
                element = ''
            else:
                element += string[i]
                i += 1
        # add the last parsed element to the list
        list_of_elements.append(element)
        return list_of_elements
