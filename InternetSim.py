import socket, sys, time

print("This is the interent Screen")
# start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", int(sys.argv[1])))
server.listen(2)
# accept connetions
conA, addrA = server.accept()
conB, addrB = server.accept()
# stop blocking
conA.setblocking(False)
conB.setblocking(False)

while True:
    dataToA, dataToB = b"", b""
    try:
        dataToB = conA.recv(1024)
    except:
        pass
    try:
        dataToA = conB.recv(1024)
    except:
        pass

    if b"q" in [dataToB, dataToA]:
        time.sleep(10)
        break
    if len(dataToB) > 0:
        print("Alice Sent To Bob:")
        print(dataToB.decode())
        conB.send(dataToB)
    if len(dataToA) > 0:
        print("Bob Sent To Alice:")
        print(dataToA.decode())
        conA.send(dataToA)

server.shutdown(socket.SHUT_RDWR)
server.close()
