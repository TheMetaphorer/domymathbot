import math
import os

VERSION = "2017.4.0_DEV"
INFO_STRING = """

----

^^^bot ^^^by ^^^u/TheMetaphorer [^^^GitHub](http://github.com/TheMetaphorer/domymathbot) ^^^Version ^^^{0}
""".format(VERSION)

OPERATORS = ['^', '!', '*', '/','%', '+', '-']
CONSTANTS = {'pi':math.pi, 'e':math.e }
FUNCTIONS = [
	'sin', 'cos', 'tan', 'log', 'ln',
	'degrees', 'radians', 'acos', 'asin',
	'atan', 'sqrt']
BASE_DIR = os.path.dirname(os.path.realpath(__file__))