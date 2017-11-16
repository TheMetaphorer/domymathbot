import re
from itertools import islice


def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)
	



class Expression:
	
	def __init__(self, expression):
		self.components = re.findall('([0-9.e]+|[\^\*\/\%\+\-\(\)\!]|pi|e)', str(expression))
		while '' in self.components: self.components.remove('')
		self.sub_expression_count = self.components.count('(') if self.components.count('(') == self.components.count(')') else 0
		
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
		
	 
  