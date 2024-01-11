from azure.storage.blob import BlobClient
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

# add your project directory to the sys.path
project_home = u'/home/hyraxmax/rh-website'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

project_folder = os.path.expanduser('~/rh-website')
load_dotenv(os.path.join(project_folder, '.env'))

today = datetime.today()
file_name = "rh-backup-" + today.strftime("%m-%d-%Y") + ".sql"

blob = BlobClient.from_connection_string(conn_str=os.getenv('AZURE_STORAGE_CONNECTION_STRING'), container_name="db-backup", blob_name=file_name)

with open("./db-backup.sql", "rb") as data:
    blob.upload_blob(data)