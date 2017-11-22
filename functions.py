import math
import utils
import settings

from components import Expression

def _operator_is_priority(expression, operator):
	operators_in_expression = [op for op in expression if op in settings.OPERATORS]
	if any(settings.PRIORITIES[op_] > settings.PRIORITIES[operator] for op_ in operators_in_expression):
		return False
	return True
	
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
		j = len(expression)-1
		for i in range(j):
			print i, len(expression)
			if i > len(expression):
				break
			if any(op in expression for op in settings.OPERATORS) == False: break
			if expression[i] in settings.OPERATORS and _operator_is_priority(expression, expression[i]):
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
			elif utils.is_printable(str(expression[i])): continue
			break
	return expression[0]

# Iterates through the expression from left to right,
# Operating on it based on the order of operations.
# Continues operating until there are no operators left
# And the expression consists of only one number (the answer).
# Known bug is the non-equivalence of certain signs in
# The order of operations, (eg. * and /, or + and -)

def _process_expression(expression, parentheses=False):
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
	if any(func in token for func in settings.FUNCTIONS for token in expression):
				for q in range(len(expression)):
					if any(func in expression[q] for func in settings.FUNCTIONS):
						f_expr_start = expression[q].index('(')+1
						f_expr_end = expression[q].index(')')
						f_expr = Expression(expression[q][f_expr_start:f_expr_end])
						f_expr_ans = float(_process_expression(f_expr)[0])
						function = [func for func in settings.FUNCTIONS if func in expression[q]][0]
						attr = getattr(math, function)
						answer=attr(f_expr_ans)
						expression[q] = answer
	if parentheses:	recursive_parentheses(expression)
	expression = _operator_evals(expression)
	return expression

# Processes an expression literally when called. 
# Execute this function by summoning u/DoMyMathBot domath
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
		logger.info('Adding comment {0} to database'.format(comment.id))
		redis_server.add_comment(comment)
	else:
		logger.warning('Request {0} does not satisfy any commands'.format(request))