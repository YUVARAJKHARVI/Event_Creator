from django.shortcuts import render
import requests
from .models import videos
from isodate import parse_duration
from time import sleep
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector

#Searching videos from Youtube
def Youtube_Search():
    while True:
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        #This will be parameters to search the videos in Youtube
        search_params = {
            'part' : 'snippet',
            'q' : 'Cricket',
            'key' : 'AIzaSyCCeAi9GVQUBQJoRqx30_v3sXfltE7U4pU',
            'maxResults' : 9,
            'type' : 'video',
            'publishedAfter':'2020-01-01T00:00:00Z'
        }
        #Getting result from Youtube
        r = requests.get(search_url, params=search_params)

        #Converting results to JSON formate
        results = r.json()['items']

        video_ids = []
        #Append the videos id to video_ids 
        for result in results:
            video_ids.append(result['id']['videoId'])
        
        #This will be parameters required videos
        video_params = {
            'key' : 'AIzaSyCCeAi9GVQUBQJoRqx30_v3sXfltE7U4pU',
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }

        #Getting result from Youtube
        r = requests.get(video_url, params=video_params)

        #Converting results to JSON formate
        results = r.json()['items']

        #For loop for store the video details in sets
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'video_link' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'description':result['snippet']['description'],
                'publishedAt':result['snippet']['publishedAt']
            }

            #Checking if already video exist
            if videos.objects.filter(id=id).exists():
                continue
            else:
                title=video_data['title']
                id=video_data['id']
                video_link=video_data['video_link']
                duration=video_data['duration']
                thumbnail=video_data['thumbnail']
                description=video_data['description']
                publishedAt=video_data['publishedAt']
                video_obj =videos.objects.create(title=title,id=id,video_link=video_link,duration=duration,thumbnail=thumbnail,description=description,publishedAt=publishedAt)
                #Saves the data into database
                video_obj.save()

            #After 10 sec function will be recalled
            sleep(10)


#Getting videos from database
def Get_Videos(request):
    #Collecting object from videos object in descending order
    video_list = videos.objects.all().order_by('-publishedAt')
    page = request.GET.get('page', 1)

    #Paginating the retrived data
    paginator = Paginator(video_list, 10)
    try:
        video = paginator.page(page)
    except PageNotAnInteger:
        video = paginator.page(1)
    except EmptyPage:
        video = paginator.page(paginator.num_pages)

    #Return the values of video to the video.html page
    return render(request, 'videos.html', { 'video': video })


#Searching video from database
def Video_Search(request):
    #Getting the user input content
    search=request.GEt['search']  
    #Query for searching related words or sentence in title and description
    video_obj=videos.objects.annotate(search=SearchVector('title', 'description'),).filter(search=search)
    
    return render(request, 'videos.html', { 'video_obj': video_obj })

