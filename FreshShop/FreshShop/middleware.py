from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
class MiddlewareTest(MiddlewareMixin):
    def process_request(self,request):
        username=request.GET.get("username")
        if username and username =="pp":
            return HttpResponse("404")
        print("这是process_request")

    def process_view(self,request,view_func,view_args,view_kwargs):
        print("这是process_view")

    def process_exception(self,request,exception):
        print("这是process_exception")

    def process_template_response(self,request,response):
        print("这是process_template_response")
        return response

    def process_response(self,request,response):
        print("这是process_response")
        return response