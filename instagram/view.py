from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed
from rest_framework.response import Response
import os
from .settings import MEDIA_ROOT
from uuid import uuid4
from content.models import Feed, Reply, Like, Bookmark
from user.models import User


#APIView : To do both Clients and Servers to interact with each other
class Main(APIView):
    def get(self, request):
        feed_list = Feed.objects.all()
        print("Connected from GET From Main1")

        #이렇게 Feed들이 리스트로 담긴 feed_list를 render안에 context안에 집어넣었습니다. 
        #근데 그냥 집어넣은 게 아니라 dict로 감싸서 집어넣었는데요, dict는 사전 형태로 key-value의 데이터를 가지고 있습니다. 
        #즉 context에 사전형 데이터를 집어넣을 건데 그 사전형 데이터는 key가 feed_list고 value가 feed_list이 됩니다. 
        #context에 넣은 feed_list는 우리가 정의한 html로 넘어가게 되는데 
        #"render에 우리가 이동하고 싶은 html과 데이터를 각각 넣으면 데이터가 이동한다"라고 생각하면 됩니다.
        return render(request, 'instagram/main1.html', context=dict(feed_list=feed_list))

class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        content = request.data.get('content')
        image = uuid_name
        profile_image = request.data.get('profile_image')
        user_id = request.data.get('user_id')

        Feed.objects.create(content=content, image=image, profile_image=profile_image, user_id=user_id, like_count=0)

        return Response(status=200)