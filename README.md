# YouTube to Google Sheets Integration Tool

This project is designed to fetch video data from a specified YouTube channel and insert it into a Google Sheets spreadsheet. It makes use of the YouTube Data API to retrieve video titles, IDs, and URLs, and the Google Sheets API to manage spreadsheet data.

## Features

- Fetch video information (title, ID, URL) from a specific YouTube channel.
- Insert the fetched video data into a Google Sheets spreadsheet.
- Handle pagination to retrieve all videos from the channel.
- Store sensitive information securely and prompt for it only once.
- User-friendly interactive command-line interface.

## Setup

Before you can run the tool, you'll need to set up your environment:

1. **Google Cloud Project:** Create a project in the Google Cloud Console, enable the YouTube Data API and Google Sheets API, and create credentials for OAuth 2.0 and a service account.

2. **Service Account Key:** Download the service account key JSON file and keep it in a secure location.

3. **API Key:** Obtain an API key for the YouTube Data API.

4. **Install Dependencies:** Install the required Python packages using the `requirements.txt` file provided in this project.

```bash
pip install -r requirements.txt

```

## Configuration:
During the first run, the tool will prompt you for the path to your service account key JSON file and your YouTube API key. It will store these securely in a config.json file for future use. Ensure config.json and any sensitive files are added to .gitignore.

## Usage
Run the script from the command line:

Copy code
```python script.py```
Follow the interactive prompts to choose a Google Sheets spreadsheet, enter a YouTube channel name, and start the video data import process.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


### requirements.txt

```
gspread>=3.0.0
google-auth>=1.0.0
google-auth-oauthlib>=0.0.0
google-api-python-client>=1.0.0
```
