import sys
import os

print(len(sys.argv))

for i in range(1, len(sys.argv)):
    os.system("nohup python3 main.py " + sys.argv[i] + " " + str(i - 2) + " " + str(i) + " > nohup" + str(i) + ".log &")