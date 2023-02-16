#!/usr/bin/python3

import psutil
import subprocess
import getopt, sys
import os, time
from datetime import datetime as dt

# Author: Andrei Egorov
# Email:  egorow777@gmail.com

disk = None
fileSize = int(1) # kb
fileCount = int(2)
fillFrom = "/dev/zero"
dateStamp = dt.now().isoformat()
fillTheFile = {} 
timeCouner = 0

###
# Print help for CLI
def usage():
  print("\nUse arguments or default variables will be set\n")
  print('Usage example: '+"\n"+sys.argv[0]+' [OPTIONAL] --file-size 10 (or --file-size-mb) --file-count 2  --fill-from=./file.txt')
  print('--help -h to see that help :D')
  print("\nOptions:\n--file-size\n Specify file size in bytes")
  print("\n--file-size-mb\n Specify file size in mb")
  print("\n--file-count\n Specify count of files")
  print("\n--fill-from\n Specify source of data for dd command")
  print("\n")

###
# CLI options
try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "file-size=", "file-count=", "fill-from=", "file-size-mb="])
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("--file-size"):
        fileSize = int(a)
    elif o in ("--file-count"):
        fileCount = int(a)
    elif o in ("--fill-from"):
        fillFrom = str(a)
    elif o in ("--file-size-mb"):
        fileSize = int(a) * 1000

##
# Show help for cli anyway
usage()

# general size for all files + 100mb should be left additionally 
minSize = fileSize * fileCount + (100000)

###
# Check disks and space
# -l flag means local. A command below will fail if a disk is not local
partitions = psutil.disk_partitions()
dfAndArgs = ["df", "-l"]

for p in partitions:
  dfAndArgs += p.mountpoint
  isRemote = subprocess.run(dfAndArgs, stdout=subprocess.DEVNULL)
  isRemoteReternCode = isRemote.returncode
  dfAndArgs = ["df", "-l"]
  if minSize < int(psutil.disk_usage(p.mountpoint).free) * 1000 and isRemoteReternCode == 0:
    disk = p.mountpoint
    break

if disk == None:
    print("There is no available disks! Check the files size")
    sys.exit(2)

###
# Make unique path for artifacts per each run
fullPath = str(disk) + "/testTaskArtifacts/" + dateStamp

### 
# We have to have access to operate with artifacts
try:
    os.makedirs(fullPath, exist_ok=True)
except OSError as err:
    print(err)
    print("\nWarning!\n")
    print("Unable to create a folder in "+disk+" mountpoint.\nMay be don't have enough rights? Create the folder and try again")
    sys.exit(2)

fullDdCmd = ["dd", "if=" + fillFrom] + ["ibs=1k", "count=" + str(fileSize) ]

###
# subprocess.Popen is pawning ssh processes in parallel and don't wait any answer.
for counter in range(fileCount):
    fullDdCmdLocal = fullDdCmd + ["of=" + fullPath + "/" + "artifact" + str(counter)]
    print(fullDdCmdLocal)
    fillTheFile[counter] = subprocess.Popen(fullDdCmdLocal, close_fds=True, stdout=subprocess.DEVNULL)

###
# Waiting for returncode, counts time and shows processes stdouts
for counter in range(fileCount):
    fillTheFile[counter].poll()
    rc = fillTheFile[counter].returncode
    while rc == None:
        time.sleep(0.1)
        timeCouner += 0.1
        fillTheFile[counter].poll()
        rc = fillTheFile[counter].returncode

print("\nThe process has taken in seconds: ", timeCouner)
print("\nfiles:")
lsCmd = subprocess.run(["ls", fullPath])

print("fillFrom: ", fillFrom)
print("Min local disk size:", minSize, "Kb")
print("Used disk:", disk)

sys.exit(0)