Readme

Requirements:
* Only for unix OS ( I was testing only on ubuntu 20.04 )
* Use Python 3 ( I was testing only on Python 3.8.10 )

Please use inventory file to specify hosts. 


Usage: ./pssh.py [OPTIONAL] --inventory ./inventory --command "lsb_release -a"

Options:
--command
    Specify command in quotes
--inventory
    Specify inventory file

P.S.
By the way! You can use pssh tool instead of the script ( https://linux.die.net/man/1/pssh )
"pssh is a program for executing ssh in parallel on a number of hosts. It provides features such as sending input to all of the processes, passing a password to ssh, saving output to files, and timing out."


**Task**:
 Run user-selected command on many servers (user-provided as param) with ssh in parallel, collect output from all nodes. The script should print collected output from all nodes on stdout, without using temp files.
