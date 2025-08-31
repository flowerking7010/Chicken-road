from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    chickens = int(data['chickens'])
    road_length = int(data['roadLength'])
    traffic = data['trafficFrequency'].lower()
    speed = int(data['vehicleSpeed'])
    weather = data['weather'].lower()
    time_of_day = data['timeOfDay'].lower()

    risk_score = 0

    # Assign weights
    if traffic == 'high': risk_score += 3
    elif traffic == 'medium': risk_score += 2
    else: risk_score += 1

    if speed > 50: risk_score += 3
    elif speed > 30: risk_score += 2
    else: risk_score += 1

    if chickens > 1: risk_score += 1
    if road_length > 15: risk_score += 1
    if weather in ['rainy', 'foggy']: risk_score += 1
    if time_of_day == 'night': risk_score += 1

    if risk_score <= 3:
        prediction = "Safe crossing"
    elif risk_score <= 6:
        prediction = "Possible delay"
    elif risk_score <= 8:
        prediction = "High risk of collision"
    else:
        prediction = "Collision likely"

    reasoning = f"Risk factors: {traffic} traffic, vehicle speed {speed} km/h, {chickens} chicken(s), {weather} weather, {time_of_day} crossing."

    return jsonify({
        "prediction": prediction,
        "reasoning": reasoning
    })

if __name__ == '__main__':
    app.run(debug=True)
