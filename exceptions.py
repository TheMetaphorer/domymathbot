

class SyntaxException(Exception):
	
	def __init__(self, *msg):
		if msg:
			super(SyntaxException, self).__init__(msg)
		else:
			super(SyntaxException, self).__init__("Invalid Syntax!")

class MissingParenthesesException(Exception):
	
	def __init__(self):
		super(MissingParenthesesException, self).__init__("You're missing a closing parentheses!")
		