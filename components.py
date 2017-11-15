import re
from itertools import islice


def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)
	



class Expression:
	
	def __init__(self, expression):
		self.components = re.findall('([0-9.e]+|[\^\*\/\%\+\-\(\)])', str(expression))
		while '' in self.components: self.components.remove('')
		self.exps = [(item, self.components[i-1], self.components[i+1]) for i, item in enumerate(self.components) if item == '^']
		self.mults = [(item, self.components[i-1], self.components[i+1]) for i, item in enumerate(self.components) if item == '*']
		self.divs = [(item, self.components[i-1], self.components[i+1]) for i, item in enumerate(self.components) if item == '/']
		self.mods = [(item, self.components[i-1], self.components[i+1]) for i, item in enumerate(self.components) if item == '%']
		self.sums = [(item, self.components[i-1], self.components[i+1]) for i, item in enumerate(self.components) if item == '+']
		self.diffs = [(item, self.components[i-1], self.components[i+1]) for i, item in enumerate(self.components) if item == '-']
		self.open_pars = [(item, self.components[i-1], self.components[i+1]) for i, item in enumerate(self.components) if item == '(']
		self.close_pars = [(item, self.components[i-1], self.components[i+1]) for i, item in enumerate(self.components) if item == ')']
		self.sub_expression_count = self.components.count('(') if self.components.count('(') == self.components.count(')') else 0
		self.total_operator_count = len(self.exps) + len(self.mults) + len(self.divs) + len(self.mods) + len(self.sums) + len(self.diffs) + len(self.open_pars)
		
	def __str__(self):
		return str(self.components)
		
	def __iter__(self):
		return self.components.__iter__()
	
	def __getitem__(self, key):
		return self.components[key]
		
	def __setitem__(self, key, value):
		self.components[key] = value
		
	def __len__(self):
		return len(self.components)
	
	def get_sum():
		return sum(self.components)
		
	def get_operator_count(self, operator):
		if operator == '^':
			return self.exps
		elif operator == '*':
			return self.mults
		elif operator == '/':
			return self.divs
		elif operator == '%':
			return self.mods
		elif operator == '+':
			return self.sums
		elif operator == '-':
			return self.diffs
		elif operator == '(':
			return self.open_pars
		elif operator == ')':
			return self.close_pars
	 
  