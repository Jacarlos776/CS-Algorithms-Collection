from collections import Counter
import os

'''
Global Variables
'''

DATASET_SIZE = 2500
TRAIN_SIZE = 1750 # (70%)
TEST_SIZE = 750 # (30%)
test_features = []
test_labels = []

train_features = []
train_labels = []

test_labels = []
header = []
k = 0
p = 0
row_count = 0

prediction_results = []
correct_predicitions = 0

'''
Functions
'''

def minkowski_distance(x1, x2, p):
    sum_of_diff_powers = 0
    for i in range(len(x1)):
        difference = abs(x1[i] - x2[i])
        power_term = difference ** p
        
        sum_of_diff_powers += power_term
        
    distance = sum_of_diff_powers ** (1/p)
    
    return distance

# gets neighbors of test instance
def get_neighbors(test_instance, training_features, training_labels, k, p):
    distances = []
    
    for i in range(len(training_features)):
        train_vector = training_features[i]
        train_label = training_labels[i]
        
        dist = minkowski_distance(test_instance, train_vector, p)
        
        distances.append((dist, train_label))
        
    
    distances.sort(key=lambda x: x[0])
    
    k_nearest_neighbors = distances[:k]
    
    return k_nearest_neighbors

# classifies wheteher it rained or did not rain
def classify_instance(neighbors):
    neighbor_labels = [label for distance, label in neighbors]
    
    label_counts = Counter(neighbor_labels)
    
    most_common_label = label_counts.most_common(1)[0][0]
    
    return most_common_label

'''
Main
'''
# get k value
while True:
    k_input = input("Please enter k-value: ")
    try:
        k = int(k_input)
        break 
    except ValueError:
        print("Invalid input. Please try again.")

# get p value
while True:
    p_input = input("Please enter 1 (Manhattan) or 2 (Euclidean) for p-value: ")
    try:
        p = int(p_input)
        if p == 1 or p == 2:
            break
        else:
            print("Please choose either 1 or 2")
    except ValueError:
        print("Invalid input. Please enter an integer (1 or 2).")

print(f"\nParameters set: k={k}, p={p}")

# move data from file to lists
input_path = os.path.join("..", "data", "KNN", "weather_forecast_data.csv")
with open(input_path, "r") as data:
    header = data.readline().strip().split(',')
    for line in data:
        current_row = line.strip().split(',')
        
        features = [float(x) for x in current_row[:-1]]
        label = current_row[-1]
        
        if row_count < TRAIN_SIZE:
            train_features.append(features)
            train_labels.append(label)
        else:
            test_features.append(features)
            test_labels.append(label)
        row_count += 1

# get neighbors, predictions, and accuracy percentage
for i in range(TEST_SIZE):
    test_instance = test_features[i]
    actual_label = test_labels[i]
    test_index = TEST_SIZE + i

    neighbors = get_neighbors(test_instance, train_features, train_labels, k, p)
    
    predicted_label = classify_instance(neighbors)
    
    is_correct = (predicted_label == actual_label)
    if is_correct:
        correct_predicitions += 1
        
    prediction_results.append({
        'index': test_index,
        'features': test_instance,
        'actual': actual_label,
        'prediction': predicted_label
    })

accuracy_percentage = (correct_predicitions / TEST_SIZE) * 100

# write to file
output_path = os.path.join("..", "data", "KNN", "output.txt")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as out:
    out.write("K-Nearest Neighbors for Weather Forecast Data\n")
    
    out.write(f"Dataset Size: {DATASET_SIZE}\n")
    out.write(f"Train Size: {TRAIN_SIZE}\n")
    out.write(f"Test Size: {TEST_SIZE}\n")
    out.write(f"k={k}, p={p}\n\n")
    
    out.write(f"Test Index      {header}                                  -> Rain\n")
    for i in range(TEST_SIZE):
        out.write(f"{i+TRAIN_SIZE+1}         {test_features[i]}         -> {prediction_results[i]['prediction']}")
        out.write(f"\n")
    out.write(f"---------------------------\n")
    out.write(f"ACCURACY: {accuracy_percentage}%")
    
    print(f"Computation successful. Check results in {output_path}")