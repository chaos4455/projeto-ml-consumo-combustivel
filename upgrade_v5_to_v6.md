# Upgrade Guide: v5 to v6

This document outlines the changes and steps required to upgrade from version v5 to v6 of the fuel consumption prediction model.

## Key Changes

* **Improved Model Accuracy:** The underlying prediction model has been further improved, resulting in even more accurate fuel consumption predictions. This involved retraining the model with an even larger and more diverse dataset, and incorporating advanced techniques to handle outliers and improve model generalization.  The model now uses a neural network architecture.  The improvement in accuracy is due to the increased capacity of the neural network to model complex non-linear relationships between the input features and the fuel consumption.

* **Enhanced API:** The API has been enhanced with new features, including batch prediction and improved error handling.  The API now supports more robust error handling and provides more detailed error messages.  The API now also includes endpoints for retrieving real-time fuel prices and predicted consumption for specific routes.  These new endpoints require integration with external APIs, which adds complexity to the API implementation.

* **New Features:** The model now incorporates additional features, such as real-time fuel prices and traffic conditions, to further enhance prediction accuracy.  These features are obtained from external APIs and integrated into the prediction model.  The integration of real-time data adds a dynamic element to the prediction process, allowing for more accurate predictions in changing conditions.

* **Improved Documentation:** The documentation has been significantly improved to provide more detailed explanations of the model, API, and upgrade process.


## Upgrade Steps

1. **Backup:** Before upgrading, back up your existing project files.

2. **Install Dependencies:** Ensure you have all the necessary dependencies installed.  Refer to the `requirements.txt` file for a complete list.  You may need to install additional libraries for the neural network model and external API integrations.  These libraries include TensorFlow/Keras or PyTorch for the neural network, and libraries for interacting with the external APIs (e.g., requests).

3. **Update Code:** Replace the old model files (`model_v5.joblib`, `predict_v5.py`) with the new model files (`model_v6.joblib`, `predict_v6.py`).  Update the API code to handle the new features and request/response formats.  This includes updating the API endpoints to handle the new features and integrating with the external APIs for real-time data.  The integration with external APIs requires careful error handling to ensure the API remains robust even if the external APIs are unavailable.

4. **Update API:** Update the API code to handle the new features and request/response formats.

5. **Test:** Thoroughly test the upgraded model and API to ensure everything is working correctly.  This includes testing the new features, error handling, and API endpoints.  The testing should include scenarios where the external APIs are unavailable or return errors.


## Mathematical Details

The v6 model uses a neural network architecture.  The specific architecture is detailed in `network_architecture.md`.  The model is trained using the Mean Squared Error (MSE) as the loss function and the Adam optimizer.  The MSE is calculated as:

**MSE = (1/n) * Σ(yᵢ - ŷᵢ)²**

Where:

* n: Number of samples
* yᵢ: Actual fuel consumption
* ŷᵢ: Predicted fuel consumption

The Adam optimizer is an adaptive learning rate optimization algorithm that is well-suited for training neural networks.  The Adam optimizer updates the weights of the neural network using the following formula:

**mₜ = β₁mₜ₋₁ + (1 - β₁)∇L(θₜ₋₁)
vₜ = β₂vₜ₋₁ + (1 - β₂)∇L(θₜ₋₁)²
m̂ₜ = mₜ / (1 - β₁ₜ)
v̂ₜ = vₜ / (1 - β₂ₜ)
θₜ = θₜ₋₁ - α * m̂ₜ / (√v̂ₜ + ε)**

Where:

* mₜ: First moment estimate (mean)
* vₜ: Second moment estimate (variance)
* β₁: Exponential decay rate for the first moment estimates (typically 0.9)
* β₂: Exponential decay rate for the second moment estimates (typically 0.999)
* ∇L(θₜ₋₁): Gradient of the loss function with respect to the parameters θ
* α: Learning rate
* ε: Small constant for numerical stability (typically 1e-8)

The learning rate α controls the step size of the weight updates.  The exponential decay rates β₁ and β₂ control the influence of past gradients on the current weight updates.  The bias correction terms (1 - β₁ₜ) and (1 - β₂ₜ) are used to compensate for the bias introduced by the exponential decay.


**Backpropagation:** The neural network is trained using backpropagation, which is an algorithm for computing the gradient of the loss function with respect to the network's weights.  The gradient is then used to update the weights using the Adam optimizer.  The backpropagation algorithm involves calculating the error at the output layer and propagating it back through the network to update the weights of each layer.
