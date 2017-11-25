

class SyntaxException(Exception):
	
	def __init__(self, *msg):
		if msg:
			super(SyntaxException, self).__init__(msg)
		else:
			super(SyntaxException, self).__init__("Invalid Syntax!")

class MissingParenthesesException(Exception):
	
	def __init__(self):
		super(MissingParenthesesException, self).__init__("You're missing a closing parentheses!")
		
		
class RedisException(Exception):
	
	def __init__(self, *msg):
		if msg:
			super(RedisException, self).__init__(msg)
		else:
			super(RedisException, self).__init__("There was a problem with redis.")
		
class RecursionException(Exception):
	
	def __init__(self, *msg):
		if msg:
			super(RecursionException, self).__init__(msg)
		else:
			super(RecursionException, self).__init__()