from matrix_ops import transpose, matrix_multiply, matrix_inverse

def process_data(data):
    X, y = [], []
    for row in data:
        if len(row) < 9:
            continue
        try:
            open_price, high_price, low_price, close_price, volume = map(
                lambda x: float(x.replace(',', '')), (row[3], row[4], row[5], row[6], row[8])
            )
            X.append([1.0, open_price, high_price, low_price, volume])
            y.append(close_price)
        except ValueError:
            continue
    theta = compute_regression(X, y)
    y_pred = predict(X, theta)
    return (X, y), (y, y_pred)

def compute_regression(X, y):
    X_T = transpose(X)
    X_T_X = matrix_multiply(X_T, X)
    X_T_X_inv = matrix_inverse(X_T_X)
    X_T_y = [[sum(a * b for a, b in zip(X_T_row, y))] for X_T_row in X_T]
    return matrix_multiply(X_T_X_inv, X_T_y)

def predict(X, theta):
    return [sum(a * b for a, b in zip(row, [t[0] for t in theta])) for row in X]


