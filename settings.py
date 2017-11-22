import math
import os

VERSION = "2017.4.1"
INFO_STRING = """

----

^^^bot ^^^by ^^^u/TheMetaphorer [^^^GitHub](http://github.com/TheMetaphorer/domymathbot) ^^^Version ^^^{0}
""".format(VERSION)

OPERATORS = ['^', '!', '*', '/','%', '+', '-']
PRIORITIES = dict(zip([op for op in OPERATORS], [0, 1, 2, 2, 2, 3, 3]))
CONSTANTS = {'pi':math.pi, 'e':math.e }
FUNCTIONS = [
	'sin', 'cos', 'tan', 'log', 'ln',
	'degrees', 'radians', 'acos', 'asin',
	'atan', 'sqrt']
BASE_DIR = os.path.dirname(os.path.realpath(__file__))