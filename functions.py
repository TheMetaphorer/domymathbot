import math
import decimal
import regex as re

import utils
import settings

from components import Expression

def _operator_is_priority(expression, operator):
	operators_in_expression = [op for op in expression if op in settings.OPERATORS]
	if any(settings.PRIORITIES[op_] < settings.PRIORITIES[operator] for op_ in operators_in_expression):
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
			if any(op in expression for op in settings.OPERATORS) == False: break
			print expression, i, j, len(expression)
			try:
				if expression[i] in settings.OPERATORS and _operator_is_priority(expression, expression[i]):
					operator = expression[i]
					print operator, _operator_is_priority(expression, operator)
					num1 = decimal.Decimal(expression[i-1])
					num2 = decimal.Decimal(expression[i+1]) if operator != '!' else None
					print expression
					if operator != '!':
						expression = _replace_values(expression, str(eval("{0}{1}{2}".format(num1, operator, num2).replace('^', '**'))), i-1, i+2)
					else:
						expression = _replace_values(expression, str(math.factorial(num1)), i-1, i+2)
				elif expression[i] in settings.CONSTANTS.keys():
					expression[i] = settings.CONSTANTS[expression[i]]
			except IndexError: break
	return expression[0]

# Iterates through the expression from left to right,
# Operating on it based on the order of operations.
# Continues operating until there are no operators left
# And the expression consists of only one number (the answer).
# Known bug is the non-equivalence of certain signs in
# The order of operations, (eg. * and /, or + and -)

def _process_expression(expression, parentheses=False):
	if len(expression) == 1 and utils.is_number(expression[0]): print expression[0]; return expression[0]
	def recursive_parentheses(expression):
		for k in range(expression.sub_expression_count):
			j = len(expression)
			for i in range(j):
				if expression[i] == '(' or expression[i] != ')':
					if '(' in expression[i+1:]:
						continue
					elif ')' in expression[i:] and expression[i] == '(':
						close_par_index=expression[i:].index(')') + i
						expression= _replace_values(expression, _operator_evals(Expression(expression[i+1:close_par_index])), i, close_par_index+1)
						break
	if any(func in token for func in settings.FUNCTIONS for token in expression):
				for q in range(len(expression)):
					if any(func in expression[q] for func in settings.FUNCTIONS):
						f_expr_start = expression[q].index('(')+1
						f_expr_end = expression[q].index(')')
						f_expr = Expression(expression[q][f_expr_start:f_expr_end])
						f_expr_ans = decimal.Decimal(_process_expression(f_expr)[0])
						function = [func for func in settings.FUNCTIONS if func in expression[q]][0]
						print function, f_expr, f_expr_ans
						if function == 'log':
							attr = getattr(math, 'log10')
						elif function == 'ln':
							attr = getattr(math, 'log')
						else:
							attr = getattr(math, function)
						answer=attr(f_expr_ans)
						expression[q] = answer
	if any(func in token for func in settings.PUBLIC_FUNCTIONS for token in expression):
				for q in range(len(expression)):
					if any(func in expression[q] for func in settings.PUBLIC_FUNCTIONS):
						f_name = [func for func in settings.PUBLIC_FUNCTIONS if func in expression[q]][0]
						f_expr = utils.BotCache('localhost', 6379, 0).get_function(f_name)
						f_args_start = expression[q].index('(')+1
						f_args_end = expression[q].index(')')
						f_args = expression[q][f_args_start:f_args_end].split(',')
						f_arg_names = re.findall('(?<![a-z])[a-z](?![a-z])', f_expr)
						for r, x in zip(f_arg_names, f_args):
							f_expr = f_expr.replace(r, x)
						f_expr_ans = decimal.Decimal(_process_expression(Expression(f_expr)))
						function = [func for func in settings.PUBLIC_FUNCTIONS if func in expression[q]][0]
						print function, f_expr, f_expr_ans
						expression[q] = f_expr_ans
	if parentheses:	recursive_parentheses(expression)
	expression = _operator_evals(expression)
	return expression

# Processes an expression literally when called. 
# Execute this function by summoning u/DoMyMathBot domath
def domath(expression):
	expression_ans = _process_expression(expression, parentheses=False if '(' not in expression else True)
	return expression_ans
	

	
def process_request(request, comment, redis_server, logger):
	# Processes a request from a user. It requires the redis_server,
	# The comment, and a logger, so that debug info can be printed.
	parsed = request.split(';')
	args = parsed[0].replace(';', '').split(' ')
	if args[1] == 'domath':
		expression = Expression(''.join(parsed[1].replace(' ', '')))
		ans = domath(expression)
		comment.reply('The answer is {0}'.format(ans) + settings.INFO_STRING)
		logger.info('Adding comment {0} to database'.format(comment.id))
		redis_server.add_comment(comment)
	elif args[1] == 'help':
		comment.reply(settings.HELP_COMMENT)
		logger.info('u/{0} requested help. Replying with help comment.'.format(comment.author.name))
		logger.info('Adding comment {0} to database'.format(comment.id))
		redis_server.add_comment(comment)
	elif args[1] == 'newfunc':
		name = args[2]
		logger.info('u/{0} requested creation of a new function {1}'.format(comment.author.name, name))
		expression = parsed[1].replace(' ', '')
		redis_server.add_function(name, expression, comment.author.name)
		redis_server.add_comment(comment)
		logger.info('Function {0} created. Expression:{1}'.format(name, expression))
		logger.info('Adding comment {0} to database'.format(comment.id))
		logger.info('Adding function {0}({1}) to database'.format(name, expression))
		comment.reply('Function {0}({1}) successfully created.'.format(name, expression))
	elif args[1] == 'delfunc':
		name = args[2]
		logger.info('u/{0} requested the deleetion of a function {1}'.format(comment.author.name, name))
		redis_server.delete_function(name, comment.author.name)
		logger.info('Function successfully deleted.')
		comment.reply('Function {0} successfully deleted.'.format(name))
		redis_server.add_comment(comment)
	else:
		logger.warning('Request {0} does not satisfy any commands'.format(request))