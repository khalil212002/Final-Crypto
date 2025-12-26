import secrets
from hashlib import sha256
from types import SimpleNamespace


class SCHNORR:
    params = SimpleNamespace(
        P=int(
            "B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C6"
            "9A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C0"
            "13ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD70"
            "98488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0"
            "A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708"
            "DF1FB2BC2E4A4371",
            16,
        ),
        Q=0xF518AA8781A8DF278ABA4E7D64B7CB9D49462353,
        G=int(
            "A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507F"
            "D6406CFF14266D31266FEA1E5C41564B777E690F5504F213"
            "160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1"
            "909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28A"
            "D662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24"
            "855E6EEB22B3B2E5",
            16,
        ),
    )

    def __init__(self, privateKey=None):
        if privateKey != None:
            self._privateKey = privateKey
            self._publicKey = pow(SCHNORR.params.G, -self._privateKey, SCHNORR.params.P)

    @staticmethod
    def generateRandomPrivateKey():
        return 1 + secrets.randbelow(SCHNORR.params.Q - 1)

    def getPublicKey(self):
        return self._publicKey

    def sign(self, message):
        k = 1 + secrets.randbelow(SCHNORR.params.Q - 1)
        r = pow(SCHNORR.params.G, k, SCHNORR.params.P)
        e = (
            int(
                sha256(
                    r.to_bytes((SCHNORR.params.P.bit_length() + 7) // 8, "big")
                    + message
                ).hexdigest(),
                16,
            )
            % SCHNORR.params.Q
        )
        s = (k + e * self._privateKey) % SCHNORR.params.Q
        return (e, s)

    def verify(self, message, signature, publicKey):
        e, s = signature
        rv = (
            pow(publicKey, e, SCHNORR.params.P)
            * pow(SCHNORR.params.G, s, SCHNORR.params.P)
            % SCHNORR.params.P
        )

        ev = (
            int(
                sha256(
                    rv.to_bytes((SCHNORR.params.P.bit_length() + 7) // 8, "big")
                    + message
                ).hexdigest(),
                16,
            )
            % SCHNORR.params.Q
        )
        return e == ev


# #example
# message = "healfasfd ijolasf j;laksfo"
# s = SCHNORR(SCHNORR.generateRandomPrivateKey())
# signature = s.sign(message.encode())
# v = SCHNORR()
# print(v.verify(message.encode(), signature, s.getPublicKey()))
