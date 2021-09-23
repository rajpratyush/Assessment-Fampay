from django.shortcuts import render
from .models import YoutubeVideoModel
from .utils import *
from .setup import *


def index(request):

    # Fetching list of videos from Youtube Data API
    video_list = youtube_query_search(QUERY, MAX_RESULTS)

    for i in range(len(video_list)):

        video = video_list[i]

        # Populating fetched video attributes into the Django YoutubeVideoModel structures
        video_object = YoutubeVideoModel(i, video[0], video[1], video[2], video[3], video[4])

        # Checking for duplicates and adding videos only if they are seen for the first time
        if video_object not in list(YoutubeVideoModel.objects.all()):
            video_object.save()

    # Getting video details in JSON format for posting on webpage
    data = get_json_data(YoutubeVideoModel.objects.all())

    # Rendering the received response onto the main webpage
    return render(request, 'index.html', {"data": data})

