import subprocess
import sys
import time

path = __file__
path = path.replace("start.py", "")
port = sys.argv[1] if (len(sys.argv) >= 2 and sys.argv[1].isnumeric) else "12345"

procceses = []
print("Starting Internet")
procceses.append(
    subprocess.Popen(
        [sys.executable, path + "InternetSim.py", port],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
)
time.sleep(1)
print("Starting Alice")
procceses.append(
    subprocess.Popen(
        [sys.executable, path + "ChatSim.py", port, "alice"],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
)
print("Starting Bob")
procceses.append(
    subprocess.Popen(
        [sys.executable, path + "ChatSim.py", port, "bob"],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
)

for p in procceses:
    p.wait()
