import os, subprocess, time

getVideos = lambda: subprocess.run(r"ls /dev | grep -P '^video\d+$'", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8").split('\n')[:-1]
def makeFakeCam():
	os.system("sudo modprobe -r v4l2loopback")
	os.system("sudo modprobe v4l2loopback")
