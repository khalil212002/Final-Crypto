def GF_SUM(a: int, b: int) -> int:
    # In GF(2^8), sum is just XOR.
    # The % 256 is technically redundant if inputs are bytes, but safe.
    return a ^ b


def GF_INV(a: int) -> int:
    """Finds multiplicative inverse of a in GF(2^8) using exponentiation."""
    # a^(-1) = a^(2^8 - 2) = a^254
    if a == 0:
        return 0
    result = 1
    for _ in range(254):
        result = GF_MUL(result, a)
    return result


def matrix_inverse(matrix):
    """Calculates the inverse of an NxN matrix in GF(2^8) using Gaussian Elimination."""
    n = len(matrix)
    # Create an augmented matrix [Matrix | Identity]
    aug = [
        row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)
    ]

    for i in range(n):
        # 1. Pivot: Find a row with non-zero element in current column
        pivot_row = i
        while pivot_row < n and aug[pivot_row][i] == 0:
            pivot_row += 1
        if pivot_row == n:
            raise ValueError("Matrix is singular (not invertible)")

        # Swap rows
        aug[i], aug[pivot_row] = aug[pivot_row], aug[i]

        # 2. Normalize pivot row so pivot element becomes 1
        inv_pivot = GF_INV(aug[i][i])
        for j in range(i, 2 * n):
            aug[i][j] = GF_MUL(aug[i][j], inv_pivot)

        # 3. Eliminate other rows
        for k in range(n):
            if k != i:
                factor = aug[k][i]
                for j in range(i, 2 * n):
                    term = GF_MUL(factor, aug[i][j])
                    aug[k][j] ^= term

    # Extract the right half (the inverse)
    inverse = [row[n:] for row in aug]
    return inverse


def GF_MUL(a, b):
    p = 0
    poly = 0x11D  # SHARK irreducible polynomial
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= poly
        b >>= 1
    return p & 0xFF


# def GF_MT_MUL(A, B):
#     # A is matrix 1, B is matrix 2
#     # Result[i][j] = Sum(A[i][k] * B[k][j])
#     size = len(A)
#     result = [[0] * size for _ in range(size)]
#     for i in range(size):
#         for j in range(size):
#             for k in range(size):
#                 # In GF(2^8), addition is XOR
#                 term = GF_MUL(A[i][k], B[k][j])
#                 result[i][j] ^= term
#     return result


def GF_MT_VEC_MUL(matrix, state_vector):
    """
    In SHARK, we usually multiply an 8x8 matrix by an 8x1 state vector.
    If state_vector is a list of 8 bytes:
    """
    result = [0] * 8
    for i in range(8):
        for j in range(8):
            result[i] ^= GF_MUL(matrix[i][j], state_vector[j])
    return result
