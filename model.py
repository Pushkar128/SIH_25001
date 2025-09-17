import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer  # <-- IMPORT THE IMPUTER
import xgboost as xgb
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

print("🚀 Loading and preparing the advanced water quality dataset...")

# 1. Load the dataset
try:
    df = pd.read_csv("data/Water_Quality_Assessment.csv")
except FileNotFoundError:
    print("❌ Error: Make sure your data is saved as 'data/Water_Quality_Assessment.csv'")
    exit()

# 2. Rename columns for consistency
rename_map = {
    'pH': 'ph', 'Dissolved Oxygen (mg/L)': 'dissolved_oxygen', 'Turbidity (NTU)': 'turbidity',
    'Electrical Conductivity (µS/cm)': 'conductivity', 'Total Dissolved Solids (TDS) (mg/L)': 'tds',
    'Nitrate (NO3⁻) (mg/L)': 'nitrate', 'Phosphate (PO4³⁻) (mg/L)': 'phosphate', 'BOD (mg/L)': 'bod',
    'COD (mg/L)': 'cod', 'Coliform Bacteria (CFU/mL)': 'coliform_bacteria', 'Ammonia (mg/L)': 'ammonia',
    'Water Quality Category': 'target'
}
df.rename(columns=rename_map, inplace=True)

# 3. Prepare data
simplified_feature_columns = [name for name in rename_map.values() if name != 'target']
df.dropna(subset=['target'], inplace=True) # Only drop rows if the target is missing
X = df[simplified_feature_columns]
y = df['target']

print(f"\n✅ Data standardized. Training with {len(simplified_feature_columns)} features.")

# 4. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 5. --- NEW: Impute missing values ---
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)
print("\n🔄 Missing values have been imputed successfully.")

# 6. Scale the IMPUTED features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)
print("⚖️ Features have been scaled successfully.")

# 7. Train the Ensemble "Committee" Model
print("⚡ Training a committee of diverse models...")
clf1 = LogisticRegression(random_state=42, max_iter=1000)
clf2 = RandomForestClassifier(n_estimators=100, random_state=42)
clf3 = xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
ensemble_model = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('xgb', clf3)], voting='hard')
ensemble_model.fit(X_train_scaled, y_train)
print("✅ Committee training complete.")

# 8. Evaluate and Save
y_pred = ensemble_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Final Ensemble Accuracy: {accuracy:.2f}")

joblib.dump(ensemble_model, "water_quality_model.pkl")
joblib.dump(simplified_feature_columns, "model_features.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(imputer, "imputer.pkl") # <-- SAVE THE IMPUTER
print("\n💾 Final model and all processing tools saved successfully!")

