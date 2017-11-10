# Do My Math Bot!

### A reddit bot by [u/TheMetaphorer](http://reddit.com/u/TheMetaphorer)

This is a bot that evaluates simple mathematic expressions. It is currently early 
in its developmental stages, so I plan to add more complex operations and capabilities
in the future. 

Currently it is able to process an operation using floating point numbers and the following operators:

^, *, /, %, +, -,

----

# Changelog:

## 2017.0.0
- Initial release.
- Follows the order of operations (does not apply equivalence to division and multiplication, or subtraction and division, so some answers may be wrong.)
- Cannot do operations on floating point numbers.

## 2017.0.1
- Removed debug print statements to improve efficiency.

## 2017.0.2
 - Fixed bug where every answer was wrong due to incorrect expression processing


## 2017.0.3
 - Added float support.
 - Improved code efficiency
 - Added specific comment reply for division by 0
 - Decreased sleep time between each coment from 10 seconds to 2.2 seconds