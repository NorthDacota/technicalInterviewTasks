#!/usr/bin/python3

import subprocess
import getopt, sys
import time

# Author: Andrei Egorov
# Email:  egorow777@gmail.com

inventory = "./inventory"
userCommand =["whoami"]
sshProc = {}
timeCouner = 0
inventoryList = []

###
# Print help for CLI
def usage():
    print("Usage:")
    print(sys.argv[0]+" --inventory ratata --command \"echo $?\"")
    print("\nOptions:\n--inventory\n Specify inventory file")
    print("\n--command\n Specify command in quotes")

###
# CLI options
try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "inventory=", "command="])
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)


for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("--inventory"):
        if a[0] == '/':
            inventory = str(a)
        else:
            inventory = "./" + str(a)
    elif o in ("--command"):
        userCommand = list(a.split(" "))

###
# Check if inventory file exists
try:
    readInventory = open(inventory, "r")
except:
    print("\nThere is no inventory file. Create and fill ./inventory or specify your own (--inventory).")

inventoryListRaw = readInventory.readlines()
readInventory.close()

###
# Allow to use comments in inventory file
for line in range(len(inventoryListRaw)):
    if not inventoryListRaw[line].startswith("#"):
        inventoryList += [inventoryListRaw[line]]

###
# Use the argument in order to pass warning with new hosts
sshCommand = ["ssh", "-oStrictHostKeyChecking=no"]

###
# Check if the inventory is empty
if inventoryList == []:
    print("Please specify at least one host in ./inventory file")
    usage()
    sys.exit(2)

###
# subprocess.Popen is pawning ssh processes in parallel and don't wait any answer.
for host in inventoryList:
    fullLocalCmd = sshCommand + [host.replace('\n', '')] + userCommand
    print("fullLocalCmd: ", fullLocalCmd)
    sshProc[host] = subprocess.Popen(fullLocalCmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 

###
# Waiting for returncode, counts time and shows processes stdouts
for host in inventoryList:
    sshProc[host].poll()
    rc = sshProc[host].returncode
    while rc == None:
        time.sleep(0.1)
        timeCouner += 0.1
        sshProc[host].poll()
        rc = sshProc[host].returncode
    stdOut = sshProc[host].communicate()
    print(host)
    print(str(stdOut[0])[2:-3],"\n")

print("Time: ", str(timeCouner)[:4], "seconds")

sys.exit(0)
