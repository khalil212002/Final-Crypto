from types import SimpleNamespace
from typing import Self


class EC:
    params = None

    def __init__(self, point: tuple[int, int]):
        self._point = point

    def getPoint(self) -> tuple[int, int]:
        return self._point

    def _add(self, p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
        if p1 == p2:
            num = (3 * p1[0] ** 2 + EC.params.a) % EC.params.p
            den = (2 * p1[1]) % EC.params.p
        else:
            num = (p2[1] - p1[1]) % EC.params.p
            den = (p2[0] - p1[0]) % EC.params.p
        if den == 0:
            return (0, 0)
        lam = (num * pow(den, -1, EC.params.p)) % EC.params.p
        x3 = (pow(lam, 2) - p1[0] - p2[0]) % EC.params.p
        y3 = (lam * (p1[0] - x3) - p1[1]) % EC.params.p
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

    def mul(self, k: int) -> Self:
        return EC(self._mul(k, self._point))

    def add(self, p: Self) -> Self:
        return EC(self._add(self._point, p.getPoint()))

    def __add__(self, other) -> Self:
        if not isinstance(other, EC):
            raise TypeError(
                f"unsupported operand type(s) for +: 'EC' and '{type(other)}'"
            )
        return self.add(other.getPoint())

    def __mul__(self, other: int) -> Self:
        if not isinstance(other, int):
            raise TypeError(
                f"unsupported operand type(s) for *: 'EC' and '{type(other)}'"
            )
        return self.mul(other)

    def __eq__(self, value) -> bool:
        if isinstance(value, tuple):
            return self._point == value
        elif isinstance(value, EC):
            return self._point == value.getPoint()
        else:
            return False

    def __str__(self):
        return "EC(" + str(self._point) + ")"

    def __repr__(self):
        return "EC(" + str(self._point) + ")"


EC.params = params = SimpleNamespace(
    p=26959946667150639794667015087019630673557916260026308143510066298881,
    a=-3,
    b=0xB4050A850C04B3ABF54132565044B0B7D7BFD8BA270B39432355FFB4,
    G=EC(
        (
            0xB70E0CBD6BB4BF7F321390B94A03C1D356C21122343280D6115C1D21,
            0xBD376388B5F723FB4C22DFE6CD4375A05A07476444D5819985007E34,
        )
    ),
    n=26959946667150639794667015087019625940457807714424391721682722368061,
    h=1,
)
