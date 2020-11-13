import ast
import math
import re
import string
import threading
from _thread import interrupt_main
from contextlib import contextmanager


def short_username(name):
    """
    Simplifies a username.

    :param name: full user name
    :return: first part that does not contain symbols

    >>> short_username("Name (PreviousName)")
    'Name'
    >>> short_username("John Doe | Example Lead")
    'John Doe'
    >>> short_username("Identity Case")
    'Identity Case'
    """
    return re.match(r"^([a-zA-Z ])+", name).group().strip()


def raw_words(message):
    """
    Filters punctuation from a sentence.

    :param message: message to parse
    :return: list of words

    >>> raw_words("This is a test.")
    ['This', 'is', 'a', 'test']
    >>> raw_words("A Discord-bot.")
    ['A', 'Discordbot']
    >>> raw_words("Identity Case")
    ['Identity', 'Case']
    """
    exclude = set(string.punctuation)
    return ''.join(c for c in message if c not in exclude).split(' ')


def sentence_contains(sentence, content):
    """
    Checks if a sentence contains some subsequence of words.

    :param sentence: sentence to search in
    :param content: part of sentence to search for
    :return: True if sentence contains content

    >>> sentence_contains("Search multiple words.", "multiple words")
    True
    >>> sentence_contains("That have to be adjacent.", "have adjacent")
    False
    >>> sentence_contains("The Discord bot.", "bot")
    True
    >>> sentence_contains("The bottom of the lake.", "bot")
    False
    >>> sentence_contains("An extra space  .", "")
    True
    >>> sentence_contains("Nothing.", "")
    False
    """
    if sentence == content: return True
    if content in sentence.split(' '): return True

    tokens = [w.lower().strip(string.punctuation) for w in sentence.split(' ')]
    content_tokens = [w.lower().strip(string.punctuation) for w in content.split(' ')]
    for i, start_token in enumerate(tokens):
        if start_token == content_tokens[0] and len(tokens) - i >= len(content_tokens):
            if all(w == w_ for w, w_ in zip(tokens[i:], content_tokens)):
                return True
    return False


def safe_to_evaluate(text_expression, max_length=300):
    """
    Check if a string could be safely evaluated by a Python interpreter.
    For now only allows simple mathematical expressions and the `math` module.

    :param text_expression: expression to test
    :param max_length: max expression length
    :return: True if the expression contains no side-effects

    >>> safe_to_evaluate("(1+2)/3 + 2**.5")
    True
    >>> safe_to_evaluate("sin(pi/2)")
    True
    >>> safe_to_evaluate("quit()")
    False
    >>> safe_to_evaluate("raise 1")
    False
    >>> safe_to_evaluate("1"*301, 300)
    False
    >>> safe_to_evaluate("x=1; x+2")
    False
    """
    if len(text_expression) > max_length:
        return False
    try:
        tree = ast.parse(text_expression)
    except SyntaxError:
        return False

    available_names = set(dir(math))
    allowed_node_types = [ast.Module, ast.Expr,
                          ast.BinOp, ast.Constant, ast.keyword,  # ast.Attribute
                          ast.Load, ast.Call,
                          ast.Div, ast.Mult, ast.Add, ast.Sub, ast.Pow]

    def inclusion_criteria(node):
        if isinstance(node, ast.Name):
            return node.id in available_names
        return any(isinstance(node, node_type) for node_type in allowed_node_types)
    return all(map(inclusion_criteria, ast.walk(tree)))


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(max_time, message="Timed out."):
    """
    Context manager that throws `TimeoutException` when the body takes too long to execute.
    
    :param max_time: maximum time in seconds
    :param message: message to include in the exception
    :return: context manager
    """
    timer = threading.Timer(max_time, interrupt_main)
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException(message)
    finally:
        timer.cancel()


def silent_eval(expression, max_execution_time=.05, max_result_length=160):
    """
    Evaluates an expression with only `math` in scope and on a time budget.
    Silences *all* exceptions and returns them as a string.

    :param expression: string expression to evaluate
    :param max_execution_time: time budget in seconds
    :param max_result_length: maximum length of result in characters
    :return: evaluated result as a string

    >>> silent_eval("100*100")
    'Result: 10000'
    >>> silent_eval("comb(8, 4)", 0.01)
    'Result: 70'
    >>> silent_eval("comb(10**8, 10**4)", 0.01)
    'Timeout: took longer than 0.01 seconds to evaluate'
    >>> silent_eval("100**100", 0.01, 200)
    'Length: evaluated expression length (201) is greater than allowed here'
    >>> silent_eval("comb()")
    'Error: comb expected 2 arguments, got 0'
    """
    try:
        with time_limit(max_execution_time):
            result = eval(expression, {}, vars(math))
    except TimeoutException:
        return f"Timeout: took longer than {max_execution_time} seconds to evaluate"
    except Exception as e:
        return f"Error: {e}"

    result_length = len(str(result))
    if result_length > max_result_length:
        return f"Length: evaluated expression length ({result_length}) is greater than allowed here"
    return f"Result: {result}"


def search(collection, matches=lambda x, y: x == y, **criteria):
    """
    Search for items matching some fields in a given collection.
    The items can have regular and integer fields, matching via some metric.

    :param collection: iterable of items
    :param matches: metric to check equality
    :param criteria: keywords of the form field_name=value, for integers field_name has to be prefixed by '_'
    :return: iterator for matching items

    >>> from math import isclose
    >>> list(search([1+1j, 0+1j, 1+0j, 0+0j], isclose, imag=0.0))
    [(1+0j), 0j]
    >>> next(search([(1, 1), (0, 1), (1, 0), (0, 0, 0)], _1=0))
    (1, 0)
    >>> set(search(['abc', 'bab', 'aba', 'aca', 'aca'], _0='a', _2='a')) == {'aba', 'aca'}
    True
    >>> list(search(['a', 'b', 'c'], _0='d'))
    []
    """
    def is_index_key(key):
        return key[0] == '_' and key[1:].isdigit()

    def get_index_key(seq, key):
        index = int(key[1:])
        return seq[index] if -len(seq) <= index < len(seq) else None

    for item in list(collection):
        if all(matches((get_index_key(item, key) if is_index_key(key) else
                       getattr(item, key, None)), value)
               for key, value in criteria.items()):
            yield item
