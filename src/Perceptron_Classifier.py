import sys
import os

# === || Helper Functions || ===

def activation(weighted_sum, threshold):
    """Return perceptron output."""
    return 1 if weighted_sum >= threshold else 0

# === || Main Algorithm || ===
def apply_perceptron(data, learning_rate, threshold, bias_input):
    """
    data = list of ([x1,x2,...], y)
    """

    n_features = len(data[0][0])
    weights = [0.0] * n_features
    wb = 0.0

    iterations_output = []
    iteration = 0

    while True:
        iteration += 1
        stable = True
        iteration_rows = []

        for x_vals, target in data:
            # compute *args
            a = sum(x * w for x, w in zip(x_vals, weights)) + wb * bias_input

            # predicted output
            y = activation(a, threshold)

            # store output row before update
            iteration_rows.append({
                "x": x_vals,
                "b_in": bias_input,
                "w": weights.copy(),
                "wb": wb,
                "a": a,
                "y": y,
                "z": target
            })

            # update rule
            if y != target:
                stable = False
                error = target - y
                # update weights
                for i in range(n_features):
                    weights[i] += learning_rate * error * x_vals[i]
                # update bias
                wb += learning_rate * error * bias_input

        iterations_output.append((iteration, iteration_rows))

        if stable:
            break

    return weights, wb, iterations_output


# === || Process Data || ===
def process_data(file_path):
    """
    Reads input.txt with format:
        0.1
        0.5
        1
        0 0 1
        0 1 1
        ...
    """
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    learning_rate = float(lines[0])
    threshold = float(lines[1])
    bias_input = float(lines[2])

    data = []
    for line in lines[3:]:
        parts = line.split()
        *features, target = parts
        x = list(map(float, features))
        y = int(target)
        data.append((x, y))

    return learning_rate, threshold, bias_input, data


# === || Format Output || ===
def output_data(weights, bias_weight, iterations_output):
    for iteration, rows in iterations_output:
        print(f"Iteration: {iteration}")

        feature_count = len(rows[0]["x"])
        header_x = " ".join([f"x{i}" for i in range(feature_count)])
        header_w = " ".join([f"w{i}" for i in range(feature_count)])

        print(f"{header_x} b {header_w} wb a y z")
        
        for row in rows:
            x_values = " ".join(str(v) for v in row["x"])
            w_values = " ".join(str(w) for w in row["w"])

            print(
                f"{x_values} "
                f"{row['b_in']} "
                f"{w_values} "
                f"{row['wb']} "
                f"{row['a']} "
                f"{row['y']} {row['z']}"
            )

        print()
        
    # print final weights
    weight_list = " ".join(str(w) for w in weights)
    print(f"Final Adjusted Weight: {weight_list}, {bias_weight}")

# === || Main || ===
def main():
    if len(sys.argv) < 2:
        print("Usage: python carlos_exer9.py input.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    learning_rate, threshold, bias_input, data = process_data(file_path)
    final_weights, final_bias_weight, iterations_output = apply_perceptron(
        data, learning_rate, threshold, bias_input
    )

    output_data(final_weights, final_bias_weight, iterations_output)


if __name__ == "__main__":
    main()