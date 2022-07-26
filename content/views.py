from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark, Weather
from user.models import User
import os
from instagram.settings import MEDIA_ROOT

#for web_crawling_weather
import datetime
import urllib
from bs4 import BeautifulSoup
import urllib.request as req
#pprint는 딕셔너리의 데이터가 긴 경우에 좀 더 보기 편하게 보여주게 도와준다.

#for Scheduling weather_status
import schedule
import time
import webbrowser

class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        # select  * from content_feed; ordey_by('-id') :reverse
        feed_object_list = Feed.objects.all().order_by('-id')
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.user_id))
            like_count = Like.objects.filter(
                feed_id=feed.id, is_like=True).count()
            is_liked = Like.objects.filter(
                feed_id=feed.id, email=email, is_like=True).exists()
            is_marked = Bookmark.objects.filter(
                feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=user.profile_image,
                                  nickname=user.user_id,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked
                                  ))

        return render(request, "instagram/main1.html", context=dict(feeds=feed_list, user=user))


class UploadFeed(APIView):
    def post(self, request):

        # 일단 파일 불러와,
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        #파일을 읽어서 만들때 쓴다고만 보면됨
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        asdf = uuid_name
        content123 = request.data.get('content')
        email = request.session.get('email', None)

        #Database
        Feed.objects.create(image=asdf, content=content123, email=email)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email)
        like_list = list(Like.objects.filter(
            email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list)
        bookmark_list = list(Bookmark.objects.filter(
            email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        return render(request, 'content/profile.html', context=dict(feed_list=feed_list,
                                                                    like_feed_list=like_feed_list,
                                                                    bookmark_feed_list=bookmark_feed_list,
                                                                    user=user))


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(
            feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        print(bookmark_text)
        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(
            feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(
                feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)


class Weather_Naver(APIView):
    def get(self, request):
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y년 %m월 %d일 %H시 %M분 입니다.')

        print("\n   Python Weather Crawling 2022 Revise\n ")
        print('   Current Datetime, ' + nowDate)
        print('   오늘의 날씨 정보입니다.\n')

        # 기상청에서 데이터를 가져옵니다.
        url = "http://www.weather.go.kr/weather/forecast/mid-term-rss3.jsp"
        res = req.urlopen(url)
        # res = req.urlopen("http://www.weather.go.kr/weather/forecast/mid-term-rss3.jsp")
        soup = BeautifulSoup(res, "html.parser")
        # Html 수프를 떠요. 우리가 지정해준 url을 파이썬이 대신 열어서 해당 html 파일을 파싱 (복사)해옵니다.
        title = soup.find("title").string
        # html 구문 분석 결과 타이틀을 가져올거에요
        weather_info = soup.find("wf").string
        print(title)
        print(weather_info)
        # 좀더 깔끔하게 표현하려면 print 함수내에 내장된 sep 기능과 텍스트 치환기능 을 활용해요
        # print(weather_info.replace("<br />","\n "),sep='\n')

        import ssl
        #네이버 날씨 크롤링
        # Phase1 Seoul Weather Crawling
        context = ssl._create_unverified_context()
        webpage = urllib.request.urlopen('https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8%EB%82%A0%EC%94%A8',context=context)
        soup = BeautifulSoup(webpage, 'html.parser')
        temps = soup.find('div','temperature_text')
        summary = soup.find('p','summary')
        #print(temps)
        # print(summary)
        summary_weather="서울 "+temps.text.strip()+summary.text.strip()
        asdf = "asdf"
        content123 = summary_weather
        email = request.session.get('email', None)
   
        #Database
        #Feed.objects.create(image=asdf, content=content123, email=email)
        Weather.objects.create(weather=asdf, content=content123, email=email)
        #return render(request, 'instagram/main1.html', {'result':summary_weather})
        return Response(status=200)