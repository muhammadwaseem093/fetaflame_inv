import os
import subprocess
import webbrowser
import time

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inve.settings")

# Start Django development server in the background
server_process = subprocess.Popen(["python", "manage.py", "runserver", "127.0.0.1:8000"])

# Give the server some time to start
time.sleep(3)

# Open the default web browser to the app
webbrowser.open("http://127.0.0.1:8000/")

# Wait for the server process to finish
server_process.wait()
