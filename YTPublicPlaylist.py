import os
import pickle  # module to save python objects as bytes and load later where required
import csv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import YoutubeFunctions as yf
from googleapiclient.discovery import build


# _________________Extracting Public Playlist_______________________
API_KEY = ''
PlayListID = 'PLEK4oGvcwpgWs8PynX7wBcsf37oDvuhlC'
service = build('youtube', 'v3', developerKey=API_KEY)
request = service.playlistItems().list(part=id, playlistId=PlayListID)
response = request.execute()
print(response)
service.close()
