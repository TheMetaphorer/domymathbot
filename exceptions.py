

class MissingParenthesesException(Exception):
	def __init__(self):
		super(MissingParenthesesException, self).__init__("You're missing a closing parentheses!")