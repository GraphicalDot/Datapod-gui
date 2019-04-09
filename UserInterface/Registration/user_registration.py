import tornado.options
import tornado.web
from SettingsModule.settings import user_collection_name, jwt_secret
from SettingsModule.cors import cors
import jwt
from LoggingModule.logging import logger



class UserRegistration(tornado.web.RequestHandler):

	def initialize(self):
			self.db = self.settings["db"]
			self.collection = self.db[user_collection_name]
			print (self.collection)

	@cors
	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def  get(self):
		self.set_status(401)
		self.finish()
		return 



			
	@cors
	@tornado.gen.coroutine
	def  post(self):
		"""
		Used to create a new user or update and existing one
		Request Param:
			user_type: admin, accessor, evaluator, superadmin
			username: 
			password: 
			newpassword:
		"""

		#print (self.request.body)

		#post_arguments = json.loads(self.request.body.decode("utf-8"))
		#print (post_arguments)
		self_image = 	self.get_body_argument("self_image", default=None, strip=False)

		adhaar_image = self.get_body_argument("adhaar_image", default=None, strip=False)






		