import socket
import threading
import sys
import time
import ECDH
import EC
from SHARK import SHARK
from SCHNORR import SCHNORR
import traceback

working = True
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
encKey = ""
verifyKey = ""


def listener():
    global working, client, verifyKey, encKey

    ver = SCHNORR()
    while working:
        data = client.recv(1024)
        if len(data) > 0:
            print("alice" if sys.argv[2] == "bob" else "alice", "sent:")
            data = eval(data.decode())
            cipher = bytes.fromhex(data[0])
            signiture = eval(data[1])
            iv = bytes.fromhex(data[2])
            msg = SHARK(encKey, iv).decrypt(cipher)
            print("Cipher text:", cipher.hex())
            print("signiture:", signiture)
            print("iv:", iv.hex())
            print("\nplain text:", msg.decode())
            sig = ver.verify(msg, signiture, verifyKey)
            print("Message signiture verified as valid:", sig, "\n")
        if b"q" in data:
            working = False
            break


def main():
    global working, client, encKey, signKey
    print("This is ", sys.argv[2], "\n")
    # connecting to server
    client.connect(("localhost", int(sys.argv[1])))

    # start schnorr
    print("\nStart SCHNORR for Signing\n")
    schnorr = SCH(client)
    # start diffie hellman
    print("\nStart Diffie Hellman For Encryption\n")
    sharedKeyEnc = DiffieHellman(client, schnorr)
    encKey = sharedKeyEnc

    print("Secure Email Started")
    # start chat
    t = threading.Thread(target=listener)
    t.start()
    while working:
        inp = input()
        if inp == "q":
            working = False
        signiture = schnorr.sign(inp.encode())
        iv = SHARK.generateRandomIv()
        cipher = SHARK(encKey, iv).encrypt(inp.encode())
        msg = (cipher.hex(), str(signiture), iv.hex())
        client.send(str(msg).encode())
    # close client
    time.sleep(1)
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    t.join()


def SCH(client):
    global verifyKey
    priv = SCHNORR.generateRandomPrivateKey()
    sch = SCHNORR(priv)
    print("Private:", hex(priv))
    print("Public:", hex(sch.getPublicKey()))
    time.sleep(1)
    client.send(str(sch.getPublicKey()).encode())
    verifyKey = int(client.recv(1024 * 4).decode())
    print("other's public key:", hex(verifyKey), "\n\n")
    return sch


def DiffieHellman(client, schnorr):
    global verifyKey
    time.sleep(1)
    private = ECDH.ECDH.generateRandomPrivateKey()
    df = ECDH.ECDH(private)
    print("Private:", private)
    print("Public:", df.getPublicKey().getPoint())
    signutre = schnorr.sign(str(df.getPublicKey().getPoint()).encode())
    print("signiture:", signutre)
    time.sleep(1)
    keyAndSign = (df.getPublicKey().getPoint(), signutre)
    client.send((str(keyAndSign)).encode())
    otherData = eval(client.recv(1024 * 4).decode())
    otherPublic = otherData[0]
    otherSigniture = otherData[1]
    print("other's public key:", otherPublic)
    df.generateSharedKey(EC.EC(otherPublic))
    print("other's signiture:", otherSigniture)
    sig = schnorr.verify(str(otherPublic).encode(), otherSigniture, verifyKey)
    print("Others public key signiture verified as valid:", sig)
    print("Shared key:", df.getSharedKey())
    hx = (
        (df.getSharedKey().getPoint()[0] ^ df.getSharedKey().getPoint()[1])
        & (2**128 - 1)
    ).to_bytes(16, "big")
    print("Shared key hex:", hx.hex(), "\n\n")
    return hx.hex()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        traceback.print_exc()
        input()
