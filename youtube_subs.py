from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyCMj71i04HM9mmr1Iwa8eDKZuPqc_PBDdo"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)


def yt_subs(token=None):
	response = youtube.subscriptions().list(part='snippet,contentDetails',channelId='UClFtGC_JLq4Drkvy3UhQT2Q',maxResults=50,order='alphabetical',pageToken=token).execute()
	return response

def get_upload_playlist(username):
	response = youtube.channels().list(part='snippet,contentDetails',id=username).execute()
	return response
	

def vids_from_playlist_id(playlistId):
	"""url_list = []
	#youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
	
	#response = youtube.channels().list(part='snippet,contentDetails',id=username).execute()
	
	#response = youtube.playlists().list(part='snippet',channelId=channel_id).execute()
	#print(response)
	#print(response)
	#uploads_playlist_url = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
	
	response = youtube.playlistItems().list(part='contentDetails',playlistId=playlistId,maxResults=1).execute()
	res = response['items']
	for i in range(len(res)):
		url_list.append(res[i]['contentDetails']['videoId'])
	return url_list"""
	pass

def search_date_user_id(userId):
	#url_list = []
	response = youtube.search().list(part='snippet',channelId=userId,order='date',maxResults=5,type='video').execute()
	return(response['items'])

def get_videos_infos(video_id):
	response_list = []
	response = youtube.videos().list(part='snippet',id=video_id).execute()
	response_list.append(response['items'][0]['snippet']['title'])
	response_list.append(response['items'][0]['snippet']['thumbnails']['default']['url'])
	response_list.append(response['items'][0]['snippet']['publishedAt'])
	response_list.append(response['items'][0]['snippet']['channelTitle'])
	return response_list