import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import config
import re

def authenticate(url='https://docs.google.com/spreadsheets/d/1XElQspBztCtSHUG6BXZVoWFetkhh9J_817rciOKcI18/edit#gid=0'):
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(config.CONFIG_PATH, gss_scopes)
    gss_client = gspread.authorize(credentials)
    sheet = gss_client.open_by_url(url)
    return sheet