import random
from EC import EC


class ECDH:

    def __init__(self, privateKey=None):
        self._privateKey = privateKey
        self._publicKey = EC.params.G * self._privateKey
        self._sharedKey = None

    @staticmethod
    def generateRandomPrivateKey() -> None:
        return random.randint(1, EC.params.n - 1)

    def generateSharedKey(self, otherPublicKey: EC) -> tuple[int, int]:
        if self._privateKey == None:
            raise Exception("Private key not generated")
        self._sharedKey = otherPublicKey * self._privateKey
        return self._sharedKey

    def getPrivateKey(self) -> int:
        if self._privateKey == None:
            raise Exception("Private key not generated")
        return self._privateKey

    def getPublicKey(self) -> EC:
        if self._publicKey == None:
            raise Exception("Public key not generated")
        return self._publicKey

    def getSharedKey(self) -> EC:
        if self._sharedKey == None:
            raise Exception("Shared key not generated")
        return self._sharedKey


# # example how to use
# alice = ECDH(ECDH.generateRandomPrivateKey())
# bob = ECDH(ECDH.generateRandomPrivateKey())

# alice.generateSharedKey(bob.getPublicKey())
# bob.generateSharedKey(alice.getPublicKey())

# print(alice.getSharedKey())
# print(bob.getSharedKey())
# print(alice.getSharedKey() == bob.getSharedKey())
