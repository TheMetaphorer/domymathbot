# Do My Math Bot!

### A reddit bot by [u/TheMetaphorer](http://reddit.com/u/TheMetaphorer)

A bot that evaluates mathematical expressions.

### How to use the bot

Summon the bot to perform a task for you with the following phrase: *u/DoMyMathBot _function_ _arguments_; _expression_* It currently supports
the following functions: _domath_, _help_, _newfunc_, _delfunc_

## u/DoMyMathBot domath; _expression_

Substitute _expression_ with your mathematical expression. It supports all the following functions from [python 2's math module:](https://docs.python.org/2/library/math.html)
sin, cos, tan, log, degrees, radians, acos, asin, atan, and sqrt, with an added ln function. Nested parentheses in functions are currently unavailable. It supports
the following mathematical operators, evaluated in the follwing order.: ^ (exponentiation), ! (factorialization), * (multiplication), / (division), % (modulus), + (addition),
 and - (subtraction). Following example of proper usage:
u/DoMyMathBot domath; (6+6.0+6.0e10)/4^2!

Improper usage:

u/DoMyMathBot 3+39-*(6+4

## u/DoMyMathBot help;

Gives a simple overview of how to use the bot. Will be improved later.

## u/DoMyMathBot newfunc _name_; _expression_

Creates a new function available to the public for everyone to use. However, only the creator of the function may delete or modify the function. 
substitute _expression_ with your formula or function, substituting arguments where necessary with a single alphabetic character. 
Currently it doesn't support naming of multiple variables of the same letter, so only a maximum of 26 variables can be used in one function. Example
using the force of attraction formula:

u/DoMyMathBot newfunc fg; (6.67e-11\*m\*n)/(r^2)

## u/DoMyMathBot delfunc _name_;

Deletes a function. Only the creator of a function may delete it.

----

# Changelog:

## 2017.5.1
- Fixed more regex matching bugs
- Cleaned up code

## 2017.5.0
- Added ability to save mathematical formulas
- Access using two new commands: newfunc and delfunc
- Added new function help
- Command syntax slightly modified. u/DoMyMathBot _command_ _arguments_; _expression_
- Fixed regex matching bugs

## 2017.4.6
- Switched support from float to Python Decimal class.

## 2017.4.5
- Removed support for round parentheses in functions
- Fixed bugs several bugs in expression string matching
- Added help comment. Request it with u/DoMyMathBot help

## 2017.4.4
- Fixed bug where bot replied to comments already replied to
- Fixed bug where ln function was not available
- Fixed bug where 'log' function returned answer in ln

## 2017.4.3
- Fixed bug where evaluating functions with a floating point number argument returned the incorrect answer

## 2017.4.2
- Fixed bug where order of operations was backwards

## 2017.4.1
- Fixed several bugs
- Remove ln function

## 2017.4.0
- Added support for mathematical functions (eg. sin, cos)

## 2017.3.0
- Changed summon keyword: summon with u/DoMyMathBot domath
- Added support for redis caching
- DoMyMathBot now bypasses comments it has already replied to
- Improved logging and debugging support

## 2017.2.3
 - Added factorial support
 - Added support for mathematical constants pi and e

## 2017.2.2
 - Removed step by step solutions

## 2017.2.1
 - Added step by step solutions for all problems

## 2017.2.0
 - Added recursive parentheses support
 - Created class for expressions, making operations more efficient while slimming code
 - Increase sleep time between each comment from 2.2 to 3 seconds

## 2017.1.1
 - Add argument passing when starting bot

## 2017.1.0
 - Added support for parentheses
 - Make domymathbot a package
 - Added exceptions module

## 2017.0.4
 - Added support for e notation for exponents

## 2017.0.3
 - Added float support.
 - Improved code efficiency
 - Added specific comment reply for division by 0
 - Decreased sleep time between each coment from 10 seconds to 2.2 seconds

## 2017.0.2
 - Fixed bug where every answer was wrong due to incorrect expression processing

## 2017.0.1
- Removed debug print statements to improve efficiency.

## 2017.0.0
- Initial release.
- Follows the order of operations (does not apply equivalence to division and multiplication, or subtraction and division, so some answers may be wrong.)
- Cannot do operations on floating point numbers.
