from apiclient.discovery import build
from .setup import *
from operator import itemgetter
import random


def get_datetime(filename):
    """Reads and generates datetime
    Youtube compatible datetime format"""

    # Opening and reading the date file
    file = open(filename, "r+")
    date = file.read()

    # Appending 0 to date if less than 10
    if int(date) < 10:
        date = "0" + date

    # Youtube compatible datetime format
    datetime = "2021-08-" + date + "T00:00:00Z"

    # Closing the file
    file.close()

    return datetime


def update_datetime(filename):
    """Updates the date in the date.txt file"""

    # Opening and reading the date
    file = open(filename, "r+")
    date = file.read()
    file.close()

    # Updating the date to some random number
    date = str(random.randint(1,31))

    # Writing updated date to the file
    file = open(filename, "w+")
    file.write(date)
    file.close()


def youtube_query_search(search_query, max_results):
    """Fetches the details of the video using the Youtube Data API"""

    # Making the Youtube Data API endpoint
    youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Fetching the date for publishedAfter date
    datetime = get_datetime(FILENAME)

    # Updating to a new date
    update_datetime(FILENAME)

    # Searching the videos on Youtube based on the given search query
    video_search = youtube_object.search().list(q=search_query, part="id, snippet", maxResults=max_results,
                                                relevanceLanguage='en', type="video", order="date",
                                                publishedAfter=datetime).execute()

    # Extract the fetched results as a list
    results = video_search.get("items", [])

    # List to store list of fetched videos in the django model parameters
    video_list = []

    # Populating video_list with videos in required format
    for result in results:

        if result['id']['kind'] == "youtube#video":

            title = result['snippet']['title']
            description = result['snippet']['description']
            thumbnails = result['snippet']['thumbnails']['default']['url']
            video_id = result['id']['videoId']
            published_date = result['snippet']['publishedAt']

            video_list.append([title, description, thumbnails, video_id, published_date])

    return video_list


def get_json_data(video_data):
    """Converts the Video object data to JSON format to display on webpage"""

    # List of videos in JSON format
    data = []

    # Populating data with JSON formats of search results
    for video in video_data:

        json = {}

        json['id'] = video.id
        json['video_title'] = video.video_title
        json['description'] = video.description
        json['video_url'] = video.video_url
        json['video_id'] = video.video_id
        json['published_date'] = video.published_date

        data.append(json)

    # Sort the JSONs in descending order of their published_dates
    data = sorted(data, key=itemgetter('published_date'), reverse=True)

    return data










