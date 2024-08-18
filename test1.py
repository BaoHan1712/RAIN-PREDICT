import pandas as pd
import numpy as np
import joblib

# Load model
loaded_svr_model = joblib.load('svr_rain.pickle')

# Load scaler 
loaded_scaler = joblib.load('scaler.pickle')

new_data = {
    'precipitation': [120],
    'water level': [0.8],
    'Soil moisture': [60]
}

new_df = pd.DataFrame(new_data)

# Chuẩn hóa data
new_data_scaled = loaded_scaler.transform(new_df)

# Predict
new_predictions = loaded_svr_model.predict(new_data_scaled)
binary_predictions = np.where(new_predictions >= 0.5, "Yes", "No")

print("Flood forecast:", binary_predictions)
print(" Predict % :", new_predictions)
