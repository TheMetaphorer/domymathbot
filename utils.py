import redis
import math

import exceptions

from string import printable

def is_printable(string):
	if any(char in printable for char in string): return True
	return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class BotCache:
	"""Cache class for do my math bot. Stores:
	Comments replied to to prevent duplicate comments
	"""
	def is_initialized(self):
		if self.redis.get('initialized') != True:
			return False
		return True
	
	def is_func(self, name):
		pass
	
	def __init__(self, host, port, db):
		self.redis = redis.Redis(host=host, port=port, db=db)
		if not self.is_initialized():
			self.redis.set('initialized', True)
			self.redis.hset('replied_comments', 'default', '0')
			self.redis.hset('functions', 'default', '0')
			
	# Adds comment to cache of all comments domymathbot has
	# replied to.
	def add_comment(self, comment):
		try:
			self.redis.hset('replied_comments', comment.id, comment.body)
		except Exception as e:
			raise  expceptions.RedisException(str(e))
	def comment_in_database(self, comment):
		data = self.redis.hkeys('replied_comments')
		if comment.id in data:
			return True
		return False
		
	def add_function(self, name, expression, user):
		if self.redis.hget('functions', name):
			raise exceptions.FunctionExists
		if self.redis.hget('function_authors', name) != user:
			raise exceptions.NotFunctionAuthor
		self.redis.hset('function_authors', name, user)
		self.redis.hset('functions', name, expression)
	
	def delete_function(self, name, user):
		if user != self.redis.hget('function_authors', name):
			raise exceptions.NotFunctionAuthor
		self.redis.hdel('functions', name)
	
	def get_function(self, name):
		return self.redis.hget('functions', name)
		
	def add_user(self, user):
		self.redis.hset('u/{0}'.format(user), 'precision', '4')
		self.redis.hset('u/{0}'.format(user), 'trigmode', 'radians')
	
	def get_users(self):
		return self.redis.scan_iter(match='u/*')
		