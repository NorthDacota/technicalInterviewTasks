###Task:
Detect locally mounted disk (make sure it is local) with at least X MB free space, create Z files of size Y, run Z “dd” processes where each process will fill the selected file with Data and print the time it took to complete the work.

Requirements:
* Only for unix OS ( I was testing only on ubuntu 20.04 )
* Use Python 3 ( I was testing only on Python 3.8.10 )
* install Requirements for python ( pip install -r requirements.txt )

Usage:
The script uses default variables unless otherwise specified.
Create testTaskArtifacts folder for the script and modify access rights. Follow by instrystions of the script and all will be fine.

./pdd.py [OPTIONAL] --file-size 10 (or --file-size-mb) --file-count 2  --fill-from=./file.txt
--help -h to see that help :D

Options:
--file-size
 Specify file size in bytes

--file-size-mb
 Specify file size in mb

--file-count
 Specify count of files

--fill-from
 Specify source of data for dd command
