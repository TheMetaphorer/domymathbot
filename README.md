# Do My Math Bot!

### A reddit bot by [u/TheMetaphorer](http://reddit.com/u/TheMetaphorer)

This is a bot that evaluates simple mathematic expressions. It is currently early 
in its developmental stages, so I plan to add more complex operations and capabilities
in the future. 

Summon the bot by commenting **u/DoMyMathBot *function* ** on a thread. Currently it is able to process an operation using floating point numbers and the following operators:

^, *, /, %, +, -,

It also has support for order of operations and parentheses. Nested parentheses work too. 
Shorthand Exponent support by using a lowercase e, not separated by spaces or any other characters, is also available. Example:

*!domath 1e9*

Will result in the bot replying that the answer is 1000000000.0 

----

# Changelog:

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
