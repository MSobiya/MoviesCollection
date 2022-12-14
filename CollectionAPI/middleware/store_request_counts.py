from CollectionAPI.models import ServerRequest
class StoreCount(object):
	def __init__(self, get_response):
		"""
		One-time configuration and initialisation.
		"""
		self.get_response = get_response

	def __call__(self, request):
		"""
		Code to be executed for each request before the view (and later
		middleware) are called.
		"""
		count = ServerRequest.objects.all().first()
		
		if not count:
			count = 1
			ServerRequest(request_count=count).save()
		else:
			ServerRequest.objects.filter(pk=count.id).update(request_count=count.request_count + 1)
		
  
		response = self.get_response(request)
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):
		"""
		Called just before Django calls the view.
		"""
		return None

	def process_exception(self, request, exception):
		"""
		Called when a view raises an exception.
		"""
		return None

	def process_template_response(self, request, response):
		"""
		Called just after the view has finished executing.
		"""
		return response

	