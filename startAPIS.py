import sys
import os

print(len(sys.argv))

for i in range(3, len(sys.argv) + 1):
    os.system("nohup python3 main.py " + sys.argv[i] + " " + str(i - 2) + " " + str(i) + " > nohup" + str(i) + ".log &")