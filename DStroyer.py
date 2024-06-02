import os
import time
import functools

"""
Usage:
1. Copy the script to the folder that you would like to scan.
2. Input "y" and the naughty MacOS files will perish.
"""

filelist = []

def clear(detection, path="."):
    # dir_list = os.listdir(path) # No longer used because of its slowness. (AVG: 8s for each scan.)
    # for i in dir_list:
    #     abspath = os.path.join(os.path.abspath(path), i)
    #     if os.path.isfile(abspath):
    #         if i.startswith(detection):
    #             print("Detected:", abspath)
    #             os.remove(abspath)
    #     if os.path.isdir(abspath):
    #         clear(detection, path=abspath)

    for fileordir in os.scandir(path):
        if fileordir.is_dir():
            clear(detection, fileordir.path)
        i = fileordir.path
        abspath = os.path.join(os.path.abspath(path), i)
        if os.path.isfile(abspath):
            if i.startswith(detection):
                print("Detected:", abspath)
                filelist.append(i)

if __name__ == '__main__':
    ret = input(f"Are you sure to delete all MacOS .DS_Store/._* files? [y/n] ")
    if ret == 'y':
        starttime = time.time()
        clear(".DS_Store", path=".")
        clear("._", path=".")
        endtime = time.time()
        print("Starting deleting...")
        for delfile in filelist:
            try:
                os.remove(delfile)
                print(f"Deleted: {delfile}")
            except Exception as e:
                print(f"Failed: {e}")
        print(f"Time Cost: {endtime-starttime:.3f}")
        print("Deletion completed.")
