import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle
import logging
from features import featureExtraction  # Uses your updated feature extraction logic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load dataset with raw URLs
data = pd.read_csv("url_dataset.csv")

# Extract features and labels
X = []
y = []
for _, row in data.iterrows():
    try:
        features = featureExtraction(row['url'])  # Extract features
        if len(features) != 13:  # Ensure 13 features
            logger.error(f"Skipping {row['url']} (incorrect feature count: {len(features)})")
            continue
        X.append(features)
        y.append(row['label'])
        logger.info(f"Processed {row['url']} with features: {features}")
    except Exception as e:
        logger.error(f"Skipping {row['url']} (error: {e})")

# Check if data is valid
if len(X) == 0:
    raise ValueError("No features extracted. Check your dataset or feature extraction logic.")

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)

# Split data into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Decision Tree
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train, y_train)
print(f"Decision Tree Accuracy: {dt_model.score(X_test, y_test):.2f}")

# Train Random Forest
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)
print(f"Random Forest Accuracy: {rf_model.score(X_test, y_test):.2f}")

# Save models
pickle.dump(dt_model, open('DecisionTree.pickle', 'wb'))
pickle.dump(rf_model, open('RandomForest.pickle', 'wb'))
print("Models saved!")