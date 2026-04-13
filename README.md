# Machine Learning Foundations & Algorithm Implementations

This repository serves as a technical portfolio of foundational artificial intelligence and machine learning algorithms. To demonstrate a deep understanding of the underlying mathematical logic and data structures, these models were implemented entirely from scratch in Python, without using high-level abstraction libraries like `scikit-learn`.

## 🚀 Featured Implementations

### Supervised Learning & Classification
* **K-Nearest Neighbors (KNN) Classifier** (`KNN_Weather_Classifier.py`)
  * **Logic:** Custom implementation utilizing Minkowski distance calculations to classify weather forecast data. Includes manual data splitting (70/30 train-test ratio) and custom voting mechanisms to determine accuracy percentages.
* **Naive Bayes Spam Filter** (`NaiveBayes_Spam_Classifier.py`)
  * **Logic:** A probabilistic classifier built using Bag-of-Words (BoW). Implements log-likelihoods and log-priors to prevent arithmetic underflow, alongside Laplace smoothing to handle unseen vocabulary in spam/ham classification.
* **Perceptron Model** (`Perceptron_Classifier.py`)
  * **Logic:** A custom single-layer neural network algorithm featuring an adjustable learning rate, threshold, and bias weight. Includes a step activation function and iterative weight adjustment logging.

### Unsupervised Learning & Clustering
* **K-Means Spatial Clustering** (`KMeans_Spatial_Clustering.py`)
  * **Logic:** Applies K-Means clustering to spatial mapping data (longitude and latitude coordinates). Computes Euclidean distances for point-to-cluster assignment and iteratively recalculates centroids. 
  * **Tools:** Integrates `pandas`, `geopandas`, and `shapely` for geospatial data handling.

### Natural Language Processing (NLP)
* **Text Preprocessing Pipeline** (`NLP_Text_Preprocessing.py`)
  * **Logic:** A foundational NLP script that cleans and tokenizes raw text data. Utilizes regex for alphanumeric filtering, Unicode normalization for accent stripping, and `collections.Counter` for efficient term frequency analysis.

### Search Algorithms & Game AI
* **Minimax Algorithm with Alpha-Beta Pruning** (`Minimax_TicTacToe_AI.py`)
  * **Logic:** An unbeatable decision-making AI for Tic-Tac-Toe. Implements the Minimax algorithm optimized with Alpha-Beta pruning to drastically reduce the number of nodes evaluated in the game tree.
* **8-Puzzle Pathfinding Solver** (`8Puzzle_AStar_Search.py` & `8Puzzle_State_Manager.py`)
  * **Logic:** A state-space search engine capable of solving the 8-puzzle problem using Breadth-First Search (BFS), Depth-First Search (DFS), and A* Search. 
  * **Heuristics:** Evaluates path costs utilizing custom heuristic functions (e.g., number of misplaced tiles) to optimize traversal efficiency.

## 🛠️ Tech Stack & Libraries
While the core algorithmic logic is written from scratch, the following libraries are utilized for data handling, mathematical operations, and environment management:
* **Core:** `Python`, `NumPy`, `math`
* **Data Processing:** `Pandas`, `collections.Counter`, `re` (Regex)
* **Geospatial & Visualization:** `GeoPandas`, `Shapely`, `Matplotlib`, `contextily`

## ⚙️ How to Run
1. Clone the repository: 
   ```bash
   git clone [https://github.com/Jacarlos776/Machine-Learning-Foundations.git](https://github.com/Jacarlos776/Machine-Learning-Foundations.git)