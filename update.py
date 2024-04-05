import requests
import tkinter.messagebox
import subprocess
import sys
# close current process before update
subprocess.call("TASKKILL /F /IM AutoIn.exe", shell=True)
subprocess.call("TASKKILL /F /IM chromedriver.exe", shell=True)
subprocess.call("TASKKILL /F /IM chrome.exe", shell=True)

print()
print("Update start now, it may take 1-2 minutes...")
print("Please wait until a messagebox shows up...")
# get the newest version number
response = requests.get(url='http://autoin.trinalgenius.co.uk:8000/version')
ver = response.text
# download the newest version software
url = "http://autoin.trinalgenius.co.uk:8000/validate/download"
r = requests.get(url, allow_redirects=True)
open('AutoIn.exe', 'wb').write(r.content)
# show prompt, process will stop until messagebox is closed
tkinter.messagebox.showinfo("Update Finished!", "Update Finished! Current Version:v"+ver+"\nAutoIn will be opened again after you close this window.")
# start again
subprocess.Popen("AutoIn.exe")
sys.exit()