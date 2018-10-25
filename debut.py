import sys
sys.path.insert(0,"youtube_tutorial")
from youtube_videos import youtube_search
import json
import youtube_subs
import codecs
import GUI
import pafy

def get_subs_list():
	channels_name_list = []
	channelsId_list = []
	token = None
	iteration = 0
	while token == None or 'nextPageToken' in test:
		iteration += 1
		print("Iteration "+str(iteration))
		test = youtube_subs.yt_subs(token)
		if 'nextPageToken' in test:
			token = test['nextPageToken']
		items = test['items']
		
		for i in range(len(items)):
			channels_name_list.append((items[i]['snippet']['title']))
			channelsId_list.append(items[i]['snippet']['resourceId']['channelId'])
			
	return(channels_name_list,channelsId_list)

def write_new_subs(channels_name,channelsId,playlistId):
	f = codecs.open("Channels_list.txt", 'w', encoding='utf8')
	for i in range(len(channels_name)):
		f.write(channels_name[i])
		f.write("$")
		f.write(channelsId[i])
		f.write("$")
		f.write(playlistId[i])
		f.write("\n")
	f.close()

def get_video_list_from_playlist_id(playlist_id):
	res = youtube_subs.vids_from_playlist_id(playlist_id)
	return res

def update_watched_videos_list(video_list_depaqued):
	f = open('watched_videos.txt','a')
	print("Dans fichier")
	for i in range(len(video_list_depaqued)):
		f.seek(0)
		f.write("https://www.youtube.com/watch?v=")
		print(video_list_depaqued[i])
		f.write(video_list_depaqued[i])
		f.write("\n")
	f.close()
	print("Dans fichier fait")

def get_videos_not_watched(video_list):
	list_from_file = []
	not_watched = []
	f = open('watched_videos.txt','r')
	for line in f:
		line = line[32:-1]
		list_from_file.append(line)
	f.close()
	print(len(list_from_file))
	for i in video_list:
		if i not in list_from_file:
			not_watched.append(i)
	return(not_watched)

print("Que voulez vous faire?\n(Treshold = 1 mois\n 1) Voir la liste des nouvelles videos\n 2) Updater la liste des abonnements\n 3) Mettre toutes les videos dans watched_videos.txt\n 4) Donnez les URL a la main pour telecharger les videos")
choix = int(input())
if choix == 1:
	url_list = []
	name_list = []
	picture_url_list = []
	channelsname_list = []
	channelsId_list = []
	playlistId_list = []
	channels_file = codecs.open("Channels_list.txt", 'r', encoding='utf8')
	for line in channels_file:
		if line != "\n":
			line = line.strip("\n")
			line = line.split("$")
			channelsname_list.append(line[0])
			channelsId_list.append(line[1])
			playlistId_list.append(line[2])
	channels_file.close()

	noms = []
	for i in range(len(channelsId_list)):
		print(i,channelsname_list[i])
		res = youtube_subs.search_date_user_id(channelsId_list[i])
		for i in range(len(res)):
			if res[i]['id']['kind'] == 'youtube#playlist':
				print("C'est une Playlist")
			elif res[i]['id']['kind'] == 'youtube#channel':
				print("C'est une Chaine")
			elif res[i]['id']['kind'] == 'youtube#video':
				print(res[i]['snippet']['title'])
				url_list.append(res[i]['id']['videoId'])
		print("    ")
	
	url_not_watched = get_videos_not_watched(url_list)
	print("Liste:")
	for i in range(len(url_not_watched)):
		print("https://www.youtube.com/watch?v="+url_not_watched[i])
	print("Total: "+str(len(url_not_watched)))
	update_watched_videos_list(url_not_watched)
	gui = GUI.GUI(url_not_watched,False)
		
elif choix == 2:
	channels_name, channelsId = get_subs_list()
	playlistId = []
	length = len(channelsId)
	for i in range(len(channelsId)):
		print(str(i+1)+"/"+str(length))
		res = youtube_subs.get_upload_playlist(channelsId[i])
		playlistId.append(res['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
	write_new_subs(channels_name,channelsId,playlistId)
	
elif choix == 3:
	url_list = []
	name_list = []
	picture_url_list = []
	channelsname_list = []
	channelsId_list = []
	playlistId_list = []
	channels_file = codecs.open("Channels_list.txt", 'r', encoding='utf8')
	for line in channels_file:
		if line != "\n":
			line = line.strip("\n")
			line = line.split("$")
			channelsname_list.append(line[0])
			channelsId_list.append(line[1])
			playlistId_list.append(line[2])
	channels_file.close()

	noms = []
	for i in range(len(channelsId_list)):
		print(i,channelsname_list[i])
		res = youtube_subs.search_date_user_id(channelsId_list[i])
		for i in range(len(res)):
			if res[i]['id']['kind'] == 'youtube#playlist':
				print("C'est une Playlist")
			elif res[i]['id']['kind'] == 'youtube#channel':
				print("C'est une Chaine")
			elif res[i]['id']['kind'] == 'youtube#video':
				print(res[i]['snippet']['title'])
				url_list.append(res[i]['id']['videoId'])
		print("    ")
	
	url_to_add = get_videos_not_watched(url_list)
	update_watched_videos_list(url_to_add)

elif choix == 4:
	print("Veuillez entrer l'url des videos que vous voulez telecharger selon cette structure:\nhttps://www.youtube.com/watch?v=ID---------, autre chose lancera le telechargement")
	url_list = []
	stop = 0
	while(not stop):
		url = str(raw_input())
		if len(url) == 43:
			url_list.append(url[32:])
		else:
			stop = 1
	print(url_list)
	gui = GUI.GUI(url_list,True)

elif choix == 5:
	#lis = ["l7LG15O6L2Y"]
	lis = ["_TH4SNjff40","s7nFjhEf55U","l7LG15O6L2Y"]
	#lis = ["_TH4SNjff40","s7nFjhEf55U","uCawbVE6xPg","_TH4SNjff40","s7nFjhEf55U","_TH4SNjff40","s7nFjhEf55U","h0MMUYvoZ94"]
	gui = GUI.GUI(lis,True)