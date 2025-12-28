import random
from GF import GF_INV, GF_MT_VEC_MUL, GF_SUM


class SHARK:
    MDS = [
        [0xCE, 0x95, 0x57, 0x82, 0x8A, 0x19, 0xB0, 0x66],
        [0xE7, 0xFE, 0x05, 0xD2, 0x52, 0xC1, 0x88, 0xF1],
        [0xB9, 0xDA, 0x4D, 0xD1, 0xC8, 0xD9, 0xD4, 0x40],
        [0x8B, 0x87, 0x3B, 0x06, 0xBB, 0xAF, 0x44, 0x0D],
        [0x73, 0x8D, 0xBF, 0xC6, 0xD6, 0x35, 0x1E, 0x22],
        [0x48, 0x56, 0x2D, 0x1D, 0x23, 0xB1, 0xC0, 0x4F],
        [0xD8, 0xFF, 0x27, 0x98, 0xA2, 0x5E, 0x5D, 0x3C],
        [0xAF, 0x24, 0xA6, 0x70, 0x2D, 0x7B, 0xB5, 0xA8],
    ]

    MDS_INV = [
        [0x85, 0xC6, 0xE4, 0xB6, 0x38, 0xAA, 0x45, 0x8A],
        [0xA7, 0xEC, 0x8B, 0xD9, 0x9A, 0xF7, 0x8A, 0xA6],
        [0x97, 0xA9, 0xEC, 0x95, 0xD6, 0xE8, 0x48, 0xD5],
        [0x4F, 0x15, 0xB0, 0xAD, 0xD8, 0x3C, 0xF2, 0xE4],
        [0x54, 0x28, 0x15, 0x2D, 0xFE, 0x92, 0x79, 0xB2],
        [0x49, 0x01, 0x7D, 0x05, 0xBF, 0xE7, 0x57, 0x61],
        [0x89, 0x8D, 0xC8, 0xD2, 0x36, 0x40, 0x37, 0x2D],
        [0x57, 0x9C, 0xF1, 0x4F, 0xB7, 0x86, 0x24, 0x57],
    ]

    RC = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40]

    @staticmethod
    def generateRandomKey():
        return random.randbytes(16).hex()

    def __init__(self, key, iv):
        self._iv = iv
        self._key = bytes.fromhex(key)
        self._expandKey()

    def _encryptIv(self, IV):
        out = IV
        for i in range(7):
            out = [GF_SUM(out[b], self._expandedKeyList[i][b]) for b in range(8)]
            out = [GF_INV(b) for b in out]
            out = GF_MT_VEC_MUL(SHARK.MDS, out)
        out = [GF_SUM(out[b], self._expandedKeyList[7][b]) for b in range(8)]
        out = GF_MT_VEC_MUL(SHARK.MDS_INV, out)
        return out

    def _expandKey(self):
        self._expandedKeyList = []
        self._expandedKeyList.append(self._key[:8])
        state = self._key
        for i in range(7):
            state = [GF_INV(b) for b in state]
            state = GF_MT_VEC_MUL(SHARK.MDS, state[:8]) + GF_MT_VEC_MUL(
                SHARK.MDS, state[8:]
            )
            state[0] = GF_SUM(state[0], SHARK.RC[i])
            self._expandedKeyList.append(state[8:] if i % 2 == 0 else state[:8])

    def _encryptDecrypt(self, data: bytearray):
        iv = self._encryptIv(self._iv)
        out = bytearray()
        for i in range(0, len(data), 8):
            out += bytearray(
                [GF_SUM(data[i + b], iv[b]) for b in range(min(8, len(data) - i))]
            )
            iv = self._encryptIv(iv)
        return bytearray(out)

    # def _pad(self, data: bytearray):
    #     delta = 8 - (len(data) % 8)
    #     data += bytearray([delta] * delta)
    #     return data

    # def _unpad(self, data: bytearray):
    #     delta = data[-1]
    #     return data[:-delta]

    def encrypt(self, data: bytearray):
        # data = self._pad(data)
        return self._encryptDecrypt(data)

    def decrypt(self, data: bytearray):
        # return self._unpad(self._encryptDecrypt(data))
        return self._encryptDecrypt(data)


# # Example code
# x = SHARK(SHARK.generateRandomKey(), random.randbytes(8))

# data = b"khalil test messageasdgfadsgfdsga"
# print(data, len(data))

# encrypted = x.encrypt(data)
# print(encrypted.hex(), len(encrypted))

# decrypted = x.decrypt(encrypted)
# print(decrypted)
# print(decrypted == data)
