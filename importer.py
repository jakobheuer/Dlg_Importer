# Jakob Heigl-Auer, 20.7.2020, Importer für .dlg nach URL
import sys
import os
import requests
import logging
import os.path
from os import path
from datetime import datetime
from tabulate import tabulate
import time
import timeit
import timeout_decorator

try:    #If user  wants specific log directory
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
    logging.basicConfig(filename=sys.argv[2]+'\Importer.log', level=logging.DEBUG)
except IndexError: #If user gave no log directory create standard log
    logging.basicConfig(filename='Importer.log',level=logging.DEBUG)

def dlg_check(f):               #Check if file is a DLG
    length = len(f)
    filetype = f[length-3:]     #Returns last 3 digits
    if(filetype=="DLG") or (filetype=="dlg"):
        return 1                #File is a DLG
    else:
        logging.warning("[" + current_time() + "], [" + sys.argv[1] + "\\" + f + "] is not a DLG\n")
        print("[" + current_time() + "]\t Outcome: [FAILED] \t File is not a DLG: [" + sys.argv[1] + "\\" + f + "]")
        global fails
        fails = fails + 1
        return 0

def current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")
    return(current_time)

def linecount(f):
    return len(open(sys.argv[1] + "\\"+ f).readlines())

def endImporter(bool): #Actions to perform when the importer is done
    if(bool==False): #did not crash
        print("\nFinished with directory [" + sys.argv[1] + "]")
        table = [["Number of files", numberOfFiles],
                 ["Success", numberOfFiles - alreadyImported - deletedAfterStart-fails],
                 ["Already imported", alreadyImported],
                 ["Failed",fails],
                 ["Delteted after import started", deletedAfterStart],
                 ["Lines sent", sentLines]]
        print(tabulate(table, headers=["Description", "Count"], tablefmt="pretty"))
        print("Importer stopped - finished at [" + current_time() + "]")
        logging.info("Finished importing " + sys.argv[1])
        logging.info("\n"+tabulate(table, headers=["Description", "Count"], tablefmt="pretty"))
        logging.info("-------------------------------------- Importer stopped [" + current_time() + "] --------------------------------------\n")
    elif(bool==True): #crashed
        print("\nException raised while importing [" + sys.argv[1] + "]")
        table = [["Number of files", numberOfFiles],
                 ["Success", numberOfFiles - alreadyImported - deletedAfterStart - fails],
                 ["Already imported", alreadyImported],
                 ["Failed", fails],
                 ["Delteted after import started", deletedAfterStart],
                 ["Lines sent", sentLines]]
        print(tabulate(table, headers=["Description", "Count"], tablefmt="pretty"))
        print("Importer stopped - ended at [" + current_time() + "]")
        logging.info("\n" + tabulate(table, headers=["Description", "Count"], tablefmt="pretty"))
        logging.info("-------------------------------------- Importer stopped [" + current_time() + "] --------------------------------------\n")

i=0
alreadyImported=0
deletedAfterStart=0
sentLines=0
fails=0
logging.info("-------------------------------------- Importer started ["+current_time()+"] --------------------------------------\n")
if(sys.argv[1]=="man") or (sys.argv[1]=="Man"): #Check if user needs Manual page
    print("DLG Importer - Manual\n"
          "Standard commands: (Use \"\" for paths)\n"
          " py importer.py \"PATH\\TO\\DLG_Directory\"\n"
          " py importer.py \"PATH\\TO\\DLG_Directory\" \"PATH\\TO\\LOG_Directory\" \n")
else:
    print("Importer Started, Importing from: " + sys.argv[1])
    if(path.exists(sys.argv[1])==True): #Checks if path is real directory
        files = os.listdir(sys.argv[1])
        numberOfFiles = len(files)
        for f in files:
            try:
                if not os.path.exists(sys.argv[1] + "\\Imported\\"):    #create imported directory if not exists
                    os.makedirs(sys.argv[1] + "\\Imported\\")
                    print("[" + current_time() + "],\t Created directory: [" + sys.argv[1] + "\\imported\\")
                    logging.info("[" + current_time() + "],\t Outcome: [Created imported directory]\t Directory: [" + sys.argv[1] + "\\imported\\")
                if not os.path.isdir(sys.argv[1] + "\\"+ f):
                    with open(sys.argv[1] + "\\"+ f, "rb") as a_file:
                        i = i+1
                        if(dlg_check(f)==1): # Send File
                            content = a_file.read()
                            post_data = {'value1': content}
                            response = requests.post("http://172.22.23.189:8000/sendfile", data=post_data)
                            print("[" + current_time() + "]\t Outcome: [" + response.text + "]\t Sent File: [" + sys.argv[1] + "\\" + f + "]\t" + str(i) + "/" + str(numberOfFiles))
                            logging.info("[" + current_time() + "],\t Outcome: [" + response.text + "]\t Sent File: [" + sys.argv[1] + "\\" + f + "]\t" + str(i) + "/" + str(numberOfFiles))
                            a_file.close()
                            z=(int(i)/int(numberOfFiles))*100
                            print(z)
                            test
                            if(response.text=="already-imported"):
                                alreadyImported = alreadyImported + 1
                                os.replace(sys.argv[1] + "\\"+ f, sys.argv[1] + "\\Imported\\"+ f)
                                logging.info("[" + current_time() + "],\t Moved ["+sys.argv[1] + "\\"+ f + "] to ["+sys.argv[1] + "\\Imported\\"+ f +"]\n")
                            elif(response.text=="success"):
                                sentLines = sentLines + linecount(f)
                                os.rename(sys.argv[1] + "\\" + f, sys.argv[1] + "\\Imported\\" + f)
                                logging.info("[" + current_time() + "],\t Moved ["+sys.argv[1] + "\\"+ f + "] to ["+sys.argv[1] + "\\Imported\\"+ f +"]\n")
                else: #If file is directory dont send and count as failed
                    i=i+1
                    fails=fails+1
                    logging.warning("[" + current_time() + "], [" + sys.argv[1] + "\\" + f + "] is not a DLG\n")
                    print("[" + current_time() + "]\t Outcome: [FAILED] \t File is not a DLG:: [" + sys.argv[1] + "\\" + f + "]")
            except (KeyboardInterrupt):
                logging.warning("[" + current_time() + "]\t KeyboardInterrupt")
                endImporter(True)
                raise
            except (SystemExit):
                logging.warning("[" + current_time() + "]\t SystemExit")
                endImporter(True)
                raise
            except(FileNotFoundError):
                print("[" + current_time() + "]\t["+sys.argv[1] + "\\"+ f + "] was deleted after import started")
                i=i+1
                deletedAfterStart = deletedAfterStart + 1
    elif(path.exists(sys.argv[1])==False): #If path is not a directory
        print("Error: [" + sys.argv[1] + "] wasn't found. Please check if the given path is correct.")
        logging.warning("[" + current_time() + "],\t [" + sys.argv[1] + "] wasn't found.\n")
"""
for x in range (0,5):
    b = "Loading" + "." * x
    print (b, end="\r")
    time.sleep(1)
    """
endImporter(False)