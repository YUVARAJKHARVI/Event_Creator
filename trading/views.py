
from django.shortcuts import render,redirect

from .models import ideas,event_list
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm


###########
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User,auth
from .google import Create_Service

def loged_in(request):
    return render(request,'register.html')
def cal(request):
    return render(request,'calender.html')


def register(request):
    if request.method =='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password']

        if(User.objects.filter(username=username).exists()):
            messages.info(request, 'username exist :(') 
            return render(request,'register.html')
              
        elif(User.objects.filter(email=email).exists()):
            messages.info(request, 'email exist :(') 
            return render(request,'register.html')

        else:
            user_obj =User.objects.create_user(username=username, email=email, password=password1)
            user_obj.save()
            messages.info(request, 'Account Created Successfully :)')  
            print(' user created '+username) 
            return render(request,'login_page.html')

    return render(request,'register.html')



def log_in(request):  
    if request.method =='POST':
          username=request.POST['username']
          password=request.POST['password'] 
          
          user=auth.authenticate(username=username,password=password)
          if user is not None:
              auth.login(request,user)
              print('register')
              print(user.is_superuser)
              return redirect(calender_view)
          else:
              print('user')
              messages.info(request, 'Enter valid username or password :(') 
              return redirect(log_in)
               
    return render(request,'login_page.html')

def sign_out(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    print("Logged out successfully!")
    return redirect(calender_view)
    
#########
calendarId='kjmbd8t17vrfqttgv2ek2vedog@group.calendar.google.com'
CLIENT_SECRET_FILE='client-secret.json'
API_NAME='calendar'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar.readonly']
service=Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    
def calender_view(request): 

    

   
    
    if request.method =='POST':
        if 'create' in request.POST:
            
            print(request.user.username)
            title=request.POST['title']
            desc=request.POST['desc']
            start=request.POST['start']
            end=request.POST['end']
            attendee=request.POST['attendee']
            attendee_mail=request.POST['attendee_mail']

            print(start)
            event = {
                'summary': title,
                'description': desc,
                'start': {
                    'dateTime': start,
                    'timeZone': 'Asia/Kolkata' 
                },
                'end': {
                    'dateTime': end,
                    'timeZone': 'Asia/Kolkata'
                },
                "extendedProperties": {
                    "private": {
                    "petsAllowed": True,
                    "formaldressCode": True
                    }
                    
                },
                
                'attendees': [
                    {'email':attendee_mail ,
                    'displayName':attendee},
                    
                ],
                
                'status':'confirmed',
                'transparency':'opaque',
                'colourId':4,
                'visibility':'public',
            }
            maxAttendees=5
            sendNotification=True
            sendUpdate='none'
            
            
            response = service.events().insert( 
                calendarId=calendarId,
                maxAttendees=maxAttendees,
                sendNotifications=sendNotification,
                sendUpdates=sendUpdate,
                body=event
                ).execute()
            
            result=(response)
            event_id=result['id']
            #event_saving=events_list.objects.create(event_id=event_id)
            #event_saving.save()
            print(result)
            '''
            page_token = None
            while True:
                events = service.events().list(calendarId='primary',q= "status ='confirmed'").execute()
                for event in events['items']:
                    print (event['summary'])
                page_token = events.get('nextPageToken')
                if not page_token:
                    break
                
            
            page_token=None
            list1 = service.events().list(calendarId='primary',q= "status ='confirmed'").execute()
            print(list1)
            '''
            
           
           
            if(event_id!=None):
                event_obj =event_list.objects.create(
                    event_id=event_id,
                    title=result['summary'],
                    description=result['description'],
                    html_link=result['htmlLink'],
                    created_time=result['created'],
                    updated_time=result['updated'],
                    start_time=result['start']['dateTime'],
                    end_time=result['end']['dateTime'],
                    attendee_name=result['attendees'][0]['displayName'],
                    attendee_email=result['attendees'][0]['email'],
                    creator=result['creator']['email'],
                    )
            
                event_obj.save()
                messages.info(request, 'Event Created :)') 
                return redirect(calender_view)


        if 'search_icon' in request.POST:
          
            search=request.POST['search']

            event=event_list.objects.all().filter(attendee_name=search)
            return render(request,'calender.html',{'event':event})
            
            '''
        if 'update' in request.POST:
            try:
                update_event_id=request.POST['event_id']
                title=request.POST['u_title']
                descr=request.POST['u_desc']
                start=request.POST['u_start1']
                end=request.POST['u_end1']
                u_attendee=request.POST['u_attendee']
                u_attendee_mail=request.POST['u_attendee_mail']
                email=request.user.email
            
                event_obj=event_list.objects.get()
            
                if descr == '':
                    descr=event_obj.description
                if title == '':
                    title=event_obj.title
                if start == '':
                    start=event_obj.start_time
                if end == '':
                    end=event_obj.end_time
                
                
                result = service.events().get(calendarId=calendarId,eventId=update_event_id).execute()
                result['summary']=title
                result['description']=descr
                result['start']['dateTime']=start
                print(end)
                result['end']['dateTime']=end
                result['attendees'][0]['displayName']=u_attendee
                result['attendees'][0]['email']=u_attendee_mail
                print(result['end']['dateTime'])
                service.events().update(calendarId=calendarId,eventId=update_event_id,body=result).execute()
                event_obj.title=title
                event_obj.description=descr
                event_obj.attendee_email=u_attendee_mail
                event_obj.attendee_name=u_attendee
                event_obj.start_time=start
                event_obj.end_time=end

                event_obj.save()
                messages.info(request, 'Event Updated :)') 
                return redirect(calender_view)
                
            except event_list.DoesNotExist:
                messages.info(request, 'Enter a valid event :(') 
                return redirect(calender_view)

       
        if 'delete' in request.POST:
            try:
                title=request.POST['d_title']
                descr=request.POST['d_desc']
                event_obj=event_list.objects.get(title=title,description=descr)
            
                event_id_number=event_obj.event_id

                service.events().delete(calendarId=calendarId,eventId=event_id_number).execute()
                event_obj.delete()
                messages.info(request, 'Event Deleted :)') 
                return redirect(calender_view)
            except event_list.DoesNotExist:
                messages.info(request, 'Enter a valid event :(') 
                return redirect(calender_view)
    
    if request.method =='POST':
        page_token = None
        while True:
            events = service.events().list(calendarId=calendarId, pageToken=page_token,q= "yuvaraj@gmail.com").execute()
            titles=[]
            descs=[]
            links=[]
            for ev in events['items']:
                title=ev['summary']
                desc=ev['description']
                html_link=ev['htmlLink']
                titles.append(title)
                descs.append(desc)
                links.append(html_link)
            page_token = events.get('nextPageToken')
            print(links)
            if not page_token:
                break
            context={
                'titles':titles,
                'descs':descs,
                'links':links
            }
            return render(request,'calender.html',{'titles':'titles'})
    '''
    '''
    event=None
    try:
        email=request.user.email
        if request.user.is_superuser == True:
            event=event_list.objects.all()
        else:
            event=event_list.objects.get(attendee_email=email)
    except event_list.DoesNotExist:
        event=None
    except AttributeError:
        email=None
    '''
    event=event_list.objects.all()
    return render(request,'calender.html',{'event':event})

def delete_event(request,delete_event_id):
    
    try:
       
        
        event_obj=event_list.objects.get(event_id=delete_event_id)
    
        event_id_number=event_obj.event_id
        if(event_id_number==delete_event_id):
            service.events().delete(calendarId=calendarId,eventId=delete_event_id).execute()
            event_obj.delete()
            messages.info(request, 'Event Deleted :)') 
            return redirect(calender_view)
    except event_list.DoesNotExist:
        messages.info(request, 'Enter a valid event :(') 
        return redirect(calender_view)
    
def update_event(request,update_event_id):
    if request.method =='POST':
        if 'update' in request.POST:
                try:
                    update_event_id=request.POST['event_id']
                    title=request.POST['u_title']
                    descr=request.POST['u_desc']
                    start=request.POST['u_start1']
                    end=request.POST['u_end1']
                    u_attendee=request.POST['u_attendee']
                    u_attendee_mail=request.POST['u_attendee_mail']

                    petsAllowed = request.POST.get('petsAllowed', False)

                    formaldressCode = request.POST.get('formaldressCode', False)
                
                    event_obj=event_list.objects.get(event_id=update_event_id)
                
                    if descr == '':
                        descr=event_obj.description
                    if title == '':
                        title=event_obj.title
                    if start == '':
                        start=event_obj.start_time
                    if end == '':
                        end=event_obj.end_time
                    if petsAllowed == '':
                        petsAllowed=event_obj.petsAllowed
                    if formaldressCode == '':
                        formaldressCode=event_obj.formaldressCode
                    
                    
                    result = service.events().get(calendarId=calendarId,eventId=update_event_id).execute()
                    result['summary']=title
                    result['description']=descr
                    result['start']['dateTime']=start
                    print(end)
                    result['end']['dateTime']=end
                    result['attendees'][0]['displayName']=u_attendee
                    result['attendees'][0]['email']=u_attendee_mail
                    result['extendedProperties']['private']['petsAllowed']=petsAllowed
                    result['extendedProperties']['private']['formaldressCode']=formaldressCode
                    
                    service.events().update(calendarId=calendarId,eventId=update_event_id,body=result).execute()
                    event_obj.title=title
                    event_obj.description=descr
                    event_obj.attendee_email=u_attendee_mail
                    event_obj.attendee_name=u_attendee
                    event_obj.start_time=start
                    event_obj.end_time=end
                    event_obj.petsAllowed=petsAllowed
                    event_obj.formaldressCode=formaldressCode

                    event_obj.save()
                    
                    messages.info(request, 'Event Updated :)') 
                    return redirect(calender_view)
                    
                except event_list.DoesNotExist:
                    messages.info(request, 'Enter a valid event :(') 
                    return redirect(calender_view)


    else:

        event_obj=event_list.objects.get(event_id=update_event_id)
        obj_event_id=event_obj.event_id
        if(obj_event_id==update_event_id):
            return render(request,'calender.html',{'update_event':event_obj})
        else:
            messages.info(request, 'Not valid event :(') 
            return redirect(calender_view)


            
          
    

def my_events(request):
    calendarId='kjmbd8t17vrfqttgv2ek2vedog@group.calendar.google.com'
    CLIENT_SECRET_FILE='client-secret.json'
    API_NAME='calendar'
    API_VERSION='v3'
    SCOPES=['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar.readonly']
    service=Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    email=request.user.email
    
    page_token = None
    while True:
        events = service.events().list(calendarId=calendarId, pageToken=page_token,q= email).execute()
        cards=[]
        
        for ev in events['items']:
            title=ev['summary']
            desc=ev['description']
            html_link=ev['htmlLink']
            card=[title,desc,html_link]
            cards.append(card)
            
        page_token = events.get('nextPageToken')
        print(cards)
        if not page_token:
            break
        
    return render(request,'calender.html',{'cards':cards})


    '''
    {'kind': 'calendar#event', 'etag': '"3278040272818000"', 
    'id': '0fif0u8m4tq7hbejilumh9vt8c', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MGZpZjB1OG00dHE3aGJlamlsdW1oOXZ0OGMga2ptYmQ4dDE3dnJmcXR0Z3YyZWsydmVkb2dAZw',
     'created': '2021-12-09T03:22:16.000Z', 
    'updated': '2021-12-09T03:22:16.409Z', 'summary': 'Google go', 'description': "A chance to hear more about Google's developer products.",
     'creator': {'email': 'yuvarajkharvi4111@gmail.com'}, 'organizer': {'email': 'kjmbd8t17vrfqttgv2ek2vedog@group.calendar.google.com', 'displayName': 'My Calendar', 'self': True},
      'start': {'dateTime': '2021-12-13T01:01:00Z', 'timeZone': 'Asia/Kolkata'}, 'end': {'dateTime': '2021-12-13T01:05:00Z', 'timeZone': 'Asia/Kolkata'}, 
      'visibility': 'public', 'iCalUID': '0fif0u8m4tq7hbejilumh9vt8c@google.com', 'sequence': 0,
       'attendees': [{'email': 'yuva@example.com', 'displayName': 'yuva', 'responseStatus': 'needsAction'}, {'email': 'yuvak@example.com', 'displayName': 'yuvak', 'responseStatus': 'needsAction'}], 
       'reminders': {'useDefault': True}, 'eventType': 'default'}
    '''

###########



###########




'''
#search
import requests
from isodate import parse_duration
from time import sleep
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector


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

    #video_obj=videos.objects.filter(name__unaccent__lower__trigram_similar=search,body_text__search=search)

    return render(request, 'videos.html', { 'video_obj': video_obj })

'''
# Create your views here.
def home(request): 
    ideas_list=ideas.objects.all()
    return render(request,'index.html',{'ideas_list':ideas_list})

def signin(request):
    return render(request,'login.html')

def my_idea(request):
    ideas_list=ideas.objects.all()
    return render(request,'my_idea.html',{'ideas_list':ideas_list})



def log_out(request):
    auth.logout(request)
    
    return redirect('/')

def log(request):
    ideas_list=ideas.objects.all()
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['psw']
        if(username=='yuva' and password=='yuva'):
            request.session['username']=username
            return render(request,'index.html',{'logged':username,'ideas_list':ideas_list})
        else: 
            return render(request,'login.html',{'error':'Username Or Password not matching'})
    return render(request,'index.html',{'ideas_list':ideas_list})
   

def add_idea(request):
    ideas_list=ideas.objects.all()
    if request.method =='POST':
         idea=request.POST['idea']
         job=request.POST['job']  
         crypto_type=request.POST['crypto']    
         risk=request.POST['risk']   
         target=request.POST['target']   
         loss=request.POST['loss'] 
         username=request.session['username']  
         idea_obj =ideas.objects.create(user_name=username,idea_name=idea, trade_name=job, trade_type=crypto_type, stoploss=loss,risk=risk,target=target)
         idea_obj.save()
         return render(request,'index.html',{'error':'Your idea will be posted','ideas_list':ideas_list,'logged':username})
    return render(request,'index.html',{'ideas_list':ideas_list})

