import subprocess
import time


mark_time = ""

while True:
    with open("last.txt", "r") as f:
        # last.txt contains the time when the AutoIn main process runs a monitor loop last time
        # if what is recorded in last.txt is the same as 60s before, close AutoIn and restart
        if mark_time == f.read():
            subprocess.call("TASKKILL /F /IM AutoIn.exe", shell=True)
            subprocess.call("TASKKILL /F /IM chromedriver.exe", shell=True)
            subprocess.call("TASKKILL /F /IM chrome.exe", shell=True)
            subprocess.Popen("AutoIn_Update.exe")
        else:
            mark_time = f.read()
        f.close()
    time.sleep(600)


