# matrix_multiply.py
# This program demonstrates matrix multiplication using Python.

def matrix_multiply(A, B):
    """
    Multiply two matrices A and B.

    A is an m x n matrix.
    B is an n x p matrix.
    The result C is an m x p matrix.
    """

    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    # Check whether the two matrices can be multiplied
    if cols_A != rows_B:
        raise ValueError("Matrix dimensions do not match for multiplication.")

    # Create a result matrix filled with zeros
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Matrix multiplication:
    # C[i][j] = sum(A[i][k] * B[k][j])
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C


def print_matrix(M):
    """Print a matrix row by row."""
    for row in M:
        print(row)


if __name__ == "__main__":
    # Test matrices
    A = [
        [1, 2],
        [3, 4]
    ]

    B = [
        [5, 6],
        [7, 8]
    ]

    print("Matrix A:")
    print_matrix(A)

    print("\nMatrix B:")
    print_matrix(B)

    C = matrix_multiply(A, B)

    print("\nResult of A x B:")
    print_matrix(C)

    print("\nExpected result:")
    print("[19, 22]")
    print("[43, 50]")