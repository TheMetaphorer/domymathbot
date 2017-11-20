import math
import os

VERSION = "2017.3.0"
INFO_STRING = """

----

^^^bot ^^^by ^^^u/TheMetaphorer [^^^GitHub](http://github.com/TheMetaphorer/domymathbot) ^^^Version ^^^{0}
""".format(VERSION)

OPERATORS = ['^', '!', '*', '/','%', '+', '-']
CONSTANTS = {'pi':math.pi, 'e':math.e }
BASE_DIR = os.path.dirname(os.path.realpath(__file__))