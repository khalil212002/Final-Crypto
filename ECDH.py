from types import SimpleNamespace
import random


class ECDH:
    params = SimpleNamespace(
        p=26959946667150639794667015087019630673557916260026308143510066298881,
        a=-3,
        b=0xB4050A850C04B3ABF54132565044B0B7D7BFD8BA270B39432355FFB4,
        G=(
            0xB70E0CBD6BB4BF7F321390B94A03C1D356C21122343280D6115C1D21,
            0xBD376388B5F723FB4C22DFE6CD4375A05A07476444D5819985007E34,
        ),
        n=26959946667150639794667015087019625940457807714424391721682722368061,
        h=1,
    )

    def __init__(self):
        self._privateKey = None
        self._publicKey = None
        self._sharedKey = None

    def _add(self, p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
        if p1 == p2:
            num = (3 * p1[0] ** 2 + ECDH.params.a) % ECDH.params.p
            den = (2 * p1[1]) % ECDH.params.p
        else:
            num = (p2[1] - p1[1]) % ECDH.params.p
            den = (p2[0] - p1[0]) % ECDH.params.p
        if den == 0:
            return (0, 0)
        lam = (num * pow(den, -1, ECDH.params.p)) % ECDH.params.p
        x3 = (pow(lam, 2) - p1[0] - p2[0]) % ECDH.params.p
        y3 = (lam * (p1[0] - x3) - p1[1]) % ECDH.params.p
        return (x3, y3)

    def _mul(self, k: int, p: tuple[int, int]) -> tuple[int, int]:
        if k == 0:
            return (0, 0)
        if k == 1:
            return p
        if k % 2 == 0:
            return self._mul(k // 2, self._add(p, p))
        else:
            return self._add(self._mul(k // 2, self._add(p, p)), p)

    def generatePrivateKey(self, key=None) -> None:
        if key == None:
            key = random.randint(1, ECDH.params.n - 1)
        self._privateKey = key

    def generatePublicKey(self) -> None:
        if self._privateKey == None:
            raise Exception("Private key not generated")
        self._publicKey = self._mul(self._privateKey, ECDH.params.G)

    def generateSharedKey(self, sharedKey: tuple[int, int]) -> tuple[int, int]:
        if self._privateKey == None:
            raise Exception("Private key not generated")
        self._sharedKey = self._mul(self._privateKey, sharedKey)
        return self._sharedKey

    def getPrivateKey(self) -> int:
        if self._privateKey == None:
            raise Exception("Private key not generated")
        return self._privateKey

    def getPublicKey(self) -> tuple[int, int]:
        if self._publicKey == None:
            raise Exception("Public key not generated")
        return self._publicKey

    def getSharedKey(self) -> tuple[int, int]:
        if self._sharedKey == None:
            raise Exception("Shared key not generated")
        return self._sharedKey


# #example how to use
# alice = ECDH()
# bob = ECDH()

# alice.generatePrivateKey()
# alice.generatePublicKey()

# bob.generatePrivateKey()
# bob.generatePublicKey()

# alice.generateSharedKey(bob.getPublicKey())
# bob.generateSharedKey(alice.getPublicKey())

# print(alice.getSharedKey())
# print(bob.getSharedKey())
