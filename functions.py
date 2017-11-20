import settings

from .components import Expression

def _replace_values(li, string, ind1, ind2):
	if len(li) == 3:
		return [string]
	else:
		li[ind1:ind2] = ''
		li.components.insert(ind1, string)
		return li
		
def _replace_constants(expression):
	for i in range(len(expression)):
		if expression[i] in settings.CONSTANTS.keys():
			expression[i] = settings.CONSTANTS[expression[i]]
			
def _operator_evals(expression):
	if any(token in settings.CONSTANTS.keys() for token in expression): _replace_constants(expression)
	while len(expression) > 1:
		j = len(expression)
		for i in range(j):
			if any(i in expression for i in settings.OPERATORS) == False: break
			if expression[i] in settings.OPERATORS:
				operator = expression[i]
				num1 = float(expression[i-1])
				num2 = float(expression[i+1]) if operator != '!' else None
				print expression
				if operator == '^':
					expression = _replace_values(expression, str(num1**num2), i-1, i+2)
				elif operator == '!':
					expression = _replace_values(expression, math.factorial(num1), i-1, i+1)
				elif operator == '*':
					expression = _replace_values(expression, str(num1*num2), i-1, i+2)
				elif operator == '/':
					expression = _replace_values(expression, str(num1/num2), i-1, i+2)
				elif operator == '%':
					expression = _replace_values(expression, str(num1%num2), i-1, i+2)
				elif operator == '+':
					expression = _replace_values(expression, str(num1+num2), i-1, i+2)
				elif operator == '-':
					expression = _replace_values(expression, str(num1-num2), i-1, i+2)
			elif expression[i] in settings.CONSTANTS.keys():
				expression[i] = settings.CONSTANTS[expression[i]]
	return expression[0]

def _process_expression(expression, parentheses=False):
	# Iterates through every operator in list of settings.OPERATORS to see if 
	# they occur in the expression. If they do, it performs the operations
	# however many times they occur. Then the broken down expression is
	# replaced with the evaluation.
	def recursive_parentheses(expression):
		for k in range(expression.sub_expression_count):
			j = len(expression)
			for i in range(j):
				if expression[i] == '(' or expression[i] != ')':
					if '(' in expression[i+1:]:
						continue
					elif ')' in expression[i:] and expression[i] == '(':
						close_par_index=expression[i:].index(')') + i
						expression= _replace_values(expression, _operator_evals(expression[i+1:close_par_index]), i, close_par_index+1)
						break
	if parentheses:	recursive_parentheses(expression)
	expression = _operator_evals(expression)
	return expression

def domath(expression):
	expression = _process_expression(expression, parentheses=False if '(' not in expression else True)
	return expression
	
def process_request(request, comment, redis_server, logger):
	# Processes a request from a user. It requires the redis_server,
	# The comment, and a logger, so that debug info can be printed.
	args = request.split(' ')[:2]
	if args[1] == 'domath':
		expression = Expression(''.join(request.split(' ')[2:]))
		ans = domath(expression)
		comment.reply('The answer is {0}'.format(ans) + settings.INFO_STRING)
		