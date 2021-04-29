# region__________________GET ALL PLAYLISTS ID & TITLE______________________
def getPlayListIDs(credentials, myChannelID):
    myList = {}
    service = build('youtube', 'v3', credentials=credentials)
    userinput = input('You require {} request token(s) to execute this activity. Do you want to proceed? Y/N'.format(1))
    if userinput == "Y":
        request = service.playlists().list(part='snippet', maxResults=50,
                                           channelId=myChannelID)
        response = request.execute()
        for eaList in response['items']:
            myList[eaList["id"]] = eaList['snippet']['title']
    return myList  # dictionary with ID as key and playlist title as value


# endregion....................................................................



# __________________GET ALL PLAYLISTS ID & TITLE______________________________
def getYoutubeVideos(credentials, myChannelID):
    nextPageToken = None
    youtubelink = "https://www.youtube.com/watch?v="
    myList = getPlayListIDs(credentials, myChannelID)
    userinput = input('You require {} request token(s) to execute this activity. Do you want to proceed? Y/N'.format(len(myList)))
    if userinput == "Y":
        for listid in list(myList.keys()):
            videos = []

            request = service.playlistItems().list(part="contentDetails", playlistId=listid)
            response = request.execute()
            totalitems = response["pageInfo"]["totalResults"]
            while len(videos) < totalitems:
                request = service.playlistItems().list(part="contentDetails", maxResults=50,
                                                       playlistId=listid, pageToken=nextPageToken)
                response = request.execute()
                for item in response["items"]:
                    videos.append(youtubelink + item["contentDetails"]['videoId'])
                nextPageToken = response.get('nextPageToken')
            service.close()

            with open(myList[listid] + ".csv", 'w', newline='') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                for x in videos:
                    wr.writerow([x])
    print("completed")
# ****************************************************************************





# __________________GET ALL PLAYLISTS ID & TITLE______________________________
def updateYoutubePlaylist(credentials, PlaylistFolder):
    userinput = input('You require {} request token(s) to execute this activity. Do you want to proceed? Y/N'.format(len(VideoID)))
    if userinput == "Y":
        for file in os.listdir(PlaylistFolder):
            service = build('youtube', 'v3', credentials=credentials)
            body = {'snippet': {'title': file[:-4]},
                    'privacyStatus': 'private'}
            request = service.playlists().insert(part='snippet,status',
                                                 body=body)
            request.execute()
        service.close()






def AddVideotoList(credentials, playlistID, VideoID):
    service = build('youtube', 'v3', credentials=credentials)
    userinput = input('You require {} request token(s) to execute this activity. Do you want to proceed? Y/N'.format(len(VideoID)))
    if userinput == "Y":
        for video in VideoID:
            try:
                body = {'snippet': {'playlistId': playlistID, 'resourceId': {
                    'kind': 'youtube#video', 'videoId': video}}}
                request = service.playlistItems().insert(part='snippet', body=body)
                request.execute()
            except:
                print(video + 'failed')
                pass
    service.close()

