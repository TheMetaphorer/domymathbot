import math
import os

VERSION = "2017.4.6"
INFO_STRING = """

----

^^^bot ^^^by ^^^u/TheMetaphorer [^^^GitHub](http://github.com/TheMetaphorer/domymathbot) ^^^Version ^^^{0}
""".format(VERSION)
HELP_COMMENT = """
Hi! I'm DoMyMathBot, here to do your math.
To summon me to solve an expression, mention me, followed by
the phrase "domath" and your expression." Example:

u/DoMyMathBot domath 1+1

If typing out all the capitalized letters in my name seems tedious,
case sensitivity doesn't matter to me, so don't worry!

I support the following operators. ^ (exponentiation), ! (factorialization),
* (multiplication), / (division), % (modulus division), + (addition), and
- (subtraction). Using me, you can write numbers like this: 1, 1.0, 1e6, or 1.0e6.
Unfortunately, I currently cannot work with numbers like -1, so please do not place
your negative numbers at the beginning of expressions. 

I have limited support for mathematic functions in python's math module which can be found
[here](https://docs.python.org/2/library/math.html) Currently, I cannot work with parentheses
inside of functions. 

I am always learning more and getting smarter, so please try me every so often, because
I might just surprise you!""" + INFO_STRING

OPERATORS = ['^', '!', '*', '/','%', '+', '-']
PRIORITIES = dict(zip([op for op in OPERATORS], [0, 1, 2, 2, 2, 3, 3]))
CONSTANTS = {'pi':math.pi, 'e':math.e }
FUNCTIONS = [
	'sin', 'cos', 'tan', 'log', 'ln',
	'degrees', 'radians', 'acos', 'asin',
	'atan', 'sqrt']
BASE_DIR = os.path.dirname(os.path.realpath(__file__))