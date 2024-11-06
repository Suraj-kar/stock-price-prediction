def transpose(matrix):
    """Return the transpose of a matrix."""
    return list(map(list, zip(*matrix)))

def matrix_multiply(A, B):
    """Multiply two matrices A and B."""
    result = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]
    return result

def matrix_inverse(matrix):
    """Compute the inverse of a matrix using Gaussian elimination."""
    n = len(matrix)
    identity = [[float(i == j) for i in range(n)] for j in range(n)]
    augmented = [row + identity_row for row, identity_row in zip(matrix, identity)]

    for i in range(n):
        factor = augmented[i][i]
        if factor == 0:
            raise ValueError("Matrix is not invertible")
        augmented[i] = [element / factor for element in augmented[i]]
        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                augmented[j] = [a - factor * b for a, b in zip(augmented[j], augmented[i])]

    inverse = [row[n:] for row in augmented]
    return inverse
