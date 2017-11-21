import redis
import exceptions

class BotCache:
	"""Cache class for do my math bot. Stores:
	Comments replied to to prevent duplicate comments
	"""
	def is_initialized(self):
		if self.redis.get('initialized') != True:
			return False
		return True
	
	def __init__(self, host, port, db):
		self.redis = redis.Redis(host=host, port=port, db=db)
		if not self.is_initialized():
			self.redis.set('initialized', True)
			self.redis.hset('replied_comments', 'default', '0')
			
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
		
	def add_function(self):
		pass