import joblib
import pandas as pd

# Load the trained model
model = joblib.load('model.joblib')

def predict_best_vehicle(distance):
    """Predicts the best vehicle for a given distance based on fuel economy.

    Args:
        distance: The distance to travel.

    Returns:
        A dictionary containing the predicted fuel consumption for each vehicle type and the best vehicle.  Returns an error message if the model prediction fails.
    """
    try:
        # Create a DataFrame for prediction
        data = pd.DataFrame({'distance': [distance], 'speed': [60]}) # Assuming an average speed of 60 for simplicity.  This could be improved by taking speed as input.

        # Get feature names from the trained model
        feature_names = model.feature_names_in_
        
        # Dynamically create one-hot encoded columns
        for feature in feature_names:
            if feature.startswith('vehicle_type_'):
                data[feature] = 0
        data.loc[0, 'vehicle_type_carro'] = 1 #default to carro


        # Predict consumption for each vehicle type
        predictions = {}
        for feature in feature_names:
            if feature.startswith('vehicle_type_'):
                data.loc[0, feature] = 1
                for other_feature in feature_names:
                    if other_feature.startswith('vehicle_type_') and other_feature != feature:
                        data.loc[0, other_feature] = 0
                consumption = model.predict(data)[0]
                vehicle_type = feature.replace('vehicle_type_', '')
                predictions[vehicle_type] = consumption

        # Find the best vehicle
        best_vehicle = min(predictions, key=predictions.get)

        return {
            'predictions': predictions,
            'best_vehicle': best_vehicle
        }
    except Exception as e:
        return f"Error during model prediction: {e}"


if __name__ == "__main__":
    distance = float(input("Enter the distance to travel: "))
    result = predict_best_vehicle(distance)
    if isinstance(result, dict):
        print("Predicted fuel consumption:")
        for vehicle, consumption in result['predictions'].items():
            print(f"- {vehicle}: {consumption:.2f}")
        print(f"\nBest vehicle for this distance: {result['best_vehicle']}")
    else:
        print(result)
