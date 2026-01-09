import subprocess
import sys
import time

path = __file__
path = path.replace("start.py", "")

procceses = []
print("Starting Internet")
procceses.append(
    subprocess.Popen(
        [sys.executable, path + "InternetSim.py", sys.argv[1]],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
)
time.sleep(1)
print("Starting Alice")
procceses.append(
    subprocess.Popen(
        [sys.executable, path + "ChatSim.py", sys.argv[1], "alice"],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
)
print("Starting Bob")
procceses.append(
    subprocess.Popen(
        [sys.executable, path + "ChatSim.py", sys.argv[1], "bob"],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
)

for p in procceses:
    p.wait()
