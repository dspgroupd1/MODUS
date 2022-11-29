# generic class for thread for all forums
class Thread():
	def __init__(self, url, title='sample title', content='', views=0, comments=0, created_by='sample user', date='00-00-00',
		forum='', thread_id=000):
		self.title = title
		self.content = content
		self.views = views
		self.date = date
		self.url = url
		self.created_by = created_by
		self.comments = comments
		self.thread_id = thread_id
		self.forum = forum

	def to_dict(self):
		return {
		'thread_id' : self.thread_id,
		'forum' : self.forum,
		'title' : self.title,
		'content' : self.content,
		'views' : self.views,
		'comments' : self.comments,
		'url' : self.url,
		'created_by' : self.created_by,
		'date' : self.date
		}