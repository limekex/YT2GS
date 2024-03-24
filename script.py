import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
import json
from getpass import getpass
import logging

# Set up basic logging
logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

print("Welcome to BeTA iTs YouTube to Google Sheets tool!")

# Load or create configuration
if not os.path.exists('config.json'):
    creds_path = getpass("First time setup. Please enter the path to your JSON credentials file for Google Sheets: ")
    youtube_api_key = getpass("Enter your YouTube API key: ")
    config = {'creds_path': creds_path, 'youtube_api_key': youtube_api_key}
    with open('config.json', 'w') as f:
        json.dump(config, f)
else:
    with open('config.json', 'r') as f:
        config = json.load(f)

try:
    # Authenticate with Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(config['creds_path'], scopes=scope)
    client = gspread.authorize(creds)
    print(f"Authenticated as: {creds.service_account_email}")

    # Authenticate with YouTube API
    youtube = build('youtube', 'v3', developerKey=config['youtube_api_key'])
except Exception as e:
    logging.error("Error during setup: %s", e)
    print("An error occurred during setup. Please check the logs for more information.")
    exit(1)

# List all available spreadsheets
def list_all_spreadsheets(client):
    sheets = client.openall()
    if not sheets:
        print("No spreadsheets available.")
        return None
    else:
        print("Available spreadsheets:")
        for idx, sheet in enumerate(sheets, start=1):
            print(f"{idx}. {sheet.title}")
        return sheets

# Choose a spreadsheet
def choose_spreadsheet(client):
    sheets = list_all_spreadsheets(client)
    if sheets:
        choice = int(input("Enter the number of the spreadsheet you want to use: ")) - 1
        return sheets[choice]
    else:
        return None

# Get YouTube channel ID by channel name
def get_channel_id_by_name(youtube, channel_name):
    request = youtube.search().list(part="snippet", type="channel", q=channel_name, maxResults=1)
    response = request.execute()
    if response['items']:
        return response['items'][0]['id']['channelId']
    else:
        print("No channel found with that name.")
        return None

def update_sheet_with_youtube_data(spreadsheet, channel_id):
    sheet = spreadsheet.sheet1
    # Sørg for at arket har riktige overskrifter
    headers = sheet.row_values(1)
    if headers != ["Name", "File", "URL"]:
        sheet.insert_row(["Name", "File", "URL"], 1)
    
    video_data = []  # For å samle videoinformasjon for bulk-innsetting
    nextPageToken = None
    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=nextPageToken,
            type="video"
        )
        response = request.execute()

        for item in response['items']:
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_data.append([video_title, video_id, video_url])
        
        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break  # Avslutt løkken hvis det ikke er flere sider
    
    # Bulk-innsetting av data
    if video_data:
        sheet.append_rows(video_data)



# Main interaction
spreadsheet = choose_spreadsheet(client)
if spreadsheet:
    channel_name = input("Enter the name of the YouTube channel: ")
    channel_id = get_channel_id_by_name(youtube, channel_name)
    if channel_id:
        print(f"Channel ID for '{channel_name}' is {channel_id}.")
        # Here you would call a function to update the sheet with YouTube data for the channel.
        # For brevity, this function call is commented out.
        update_sheet_with_youtube_data(spreadsheet, channel_id)
else:
    print("Exiting the program.")
