from django.shortcuts import render
from rest_framework.views import APIView


#APIView : To do both Clients and Servers to interact with each other
class Main(APIView):
    def get(self, request):
        print("Connected from GET")
        return render(request, 'instagram/main.html')

    def post(self, request):
        print("Connected from POST")
        return render(request, 'instagram/main.html')


class Main1(APIView):
    def get(self, request):
        print("Connected from GET From Main1")
        return render(request, 'instagram/main1.html')

    def post(self, request):
        print("Connected from POST")
        return render(request, 'instagram/main1.html')
