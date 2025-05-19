from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import sys
import codecs
import requests

# Fix encoding issue for Windows systems
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model
model = load_model(r"D:\Project AI Final\project\model\model_trained_101class.h5")

# Define the class map using the labels from your file
class_map = {
    idx: label for idx, label in enumerate([
        'Apple pie', 'Baby back ribs', 'Baklava', 'Beef carpaccio', 'Beef tartare',
        'Beet salad', 'Beignets', 'Bibimbap', 'Bread pudding', 'Breakfast burrito',
        'Bruschetta', 'Caesar salad', 'Cannoli', 'Caprese salad', 'Carrot cake',
        'Ceviche', 'Cheesecake', 'Cheese plate', 'Chicken curry', 'Chicken quesadilla',
        'Chicken wings', 'Chocolate cake', 'Chocolate mousse', 'Churros', 'Clam chowder',
        'Club sandwich', 'Crab cakes', 'Creme brulee', 'Croque madame', 'Cup cakes',
        'Deviled eggs', 'Donuts', 'Dumplings', 'Edamame', 'Eggs benedict', 'Escargots',
        'Falafel', 'Filet mignon', 'Fish and chips', 'Foie gras', 'French fries',
        'French onion soup', 'French toast', 'Fried calamari', 'Fried rice', 'Frozen yogurt',
        'Garlic bread', 'Gnocchi', 'Greek salad', 'Grilled cheese sandwich', 'Grilled salmon',
        'Guacamole', 'Gyoza', 'Hamburger', 'Hot and sour soup', 'Hot dog', 'Huevos rancheros',
        'Hummus', 'Ice cream', 'Lasagna', 'Lobster bisque', 'Lobster roll sandwich',
        'Macaroni and cheese', 'Macarons', 'Miso soup', 'Mussels', 'Nachos', 'Omelette',
        'Onion rings', 'Oysters', 'Pad thai', 'Paella', 'Pancakes', 'Panna cotta',
        'Peking duck', 'Pho', 'Pizza', 'Pork chop', 'Poutine', 'Prime rib',
        'Pulled pork sandwich', 'Ramen', 'Ravioli', 'Red velvet cake', 'Risotto', 'Samosa',
        'Sashimi', 'Scallops', 'Seaweed salad', 'Shrimp and grits', 'Spaghetti bolognese',
        'Spaghetti carbonara', 'Spring rolls', 'Steak', 'Strawberry shortcake', 'Sushi',
        'Tacos', 'Takoyaki', 'Tiramisu', 'Tuna tartare', 'Waffles'
    ])
}

# Nutritionix API Credentials
app_id = "ef34f3e3"
api_key = "7eeb1ab0716eb2985817786796409b0b"

def get_calories(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    headers = {
        "x-app-id": app_id,
        "x-app-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "query": food_item,
        "timezone": "US/Eastern"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        food_data = result["foods"][0]
        calories = food_data["nf_calories"]
        serving_weight = food_data["serving_weight_grams"]

        # Calculate calories per 100 grams
        calories_per_100g = (calories / serving_weight) * 100
        return f"{calories_per_100g:.2f} calories per 100 grams"
    else:
        return "Error retrieving data"

def is_good_for_diet(calories_per_100g):
    calories = float(calories_per_100g.split()[0])  # Extract calorie value
    if calories < 200:
        return "✔️ Bagus untuk diet (Rendah Kalori)"
    elif calories <= 500:
        return "⚠️ Cocok untuk diet (Sedang Kalori)"
    else:
        return "❌ Kurang cocok untuk diet (Tinggi Kalori)"

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/aboutpage')
def about_page():
    return render_template('aboutpage.html')

# Tambahkan daftar ekstensi file yang diizinkan
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """Periksa apakah file memiliki ekstensi yang valid."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        print("No file part in the request")
        return jsonify({"error": "No file uploaded"})
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"})
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only JPG, JPEG, and PNG are allowed."})
    
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)    
    
    try:
        image = load_img(file_path, target_size=(224, 224))
        image_array = img_to_array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        predictions = model.predict(image_array)
        predicted_class = class_map[np.argmax(predictions)]
        confidence = np.max(predictions)

        calorie_info = get_calories(predicted_class)
        diet_evaluation = is_good_for_diet(calorie_info)
        
        return jsonify({
            "foodName": predicted_class,
            "caloriesPerGram": calorie_info,
            "dietSuitability": diet_evaluation,
            "confidence": float(confidence)
        })
    except Exception as e:
        return jsonify({"error": f"An error occurred during prediction: {str(e)}"})
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
