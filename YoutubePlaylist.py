import os
import pickle  # module to save python objects as bytes and load later where required
import csv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import youtubeFunctions as yf
from googleapiclient.discovery import build

# region______________LOAD CREDENTIALS_________________________________
credentials = None
if os.path.exists("token.pickle"):
    print('Loading credentials from file...')
    with open("token.pickle", 'rb') as token:
        credentials = pickle.load(token)

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'OAuth.json', scopes=['https://www.googleapis.com/auth/youtube'])
        flow.run_local_server(port=3000, prompt='consent',
                              authorization_prompt_message="")
        credentials = flow.credentials
        print(credentials.to_json())

        with open("token.pickle", "wb") as futureuse:
            pickle.dump(credentials, futureuse)

# endregion __________________________________________________________
myChannelID = '_______________'

PlaylistFolder = "/Users/vignesh/Documents/CODE/Python/PYCHARM/pyYoutubeApp/Playlist_csv"

# yf.getYoutubeVideos(credentials, myChannelID)
# yf.updateYoutubePlaylist(credentials, PlaylistFolder)

AllPlayList = yf.getPlayListIDs(credentials, myChannelID)
# print(AllPlayList)
AllPlayList = {y: x for x, y in AllPlayList.items()}
for file in os.listdir(PlaylistFolder):
    filepath = PlaylistFolder + '/' + file
    print(filepath)
    f = open(filepath)
    ReadCSV = csv.reader(f)
    VideoList = list(ReadCSV)
    VideoList = [VideoList[i][0] for i in range(len(VideoList))]
    VideoID = [vidID.split("https://www.youtube.com/watch?v=")[1]
               for vidID in VideoList]
    yf.AddVideotoList(credentials, AllPlayList[file[:-4]], VideoID)

# _____________________Sample for public data_______________________
# API_KEY = ''

# service = build('youtube', 'v3', developerKey=API_KEY)
# request = service.playlistItems().list(
#     part=id, playlistId='PLEK4oGvcwpgWs8PynX7wBcsf37oDvuhlC')
# response = request.execute()
# print(response)
# service.close()
