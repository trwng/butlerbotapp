import time
import requests
import json
import pyttsx3



APP_ID = "d1b56ee3"
API_KEY = "1952289073a5f8e6f532f465abf99951"

HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

SEARCH_URL = "https://trackapi.nutritionix.com/v2/search/instant"
ITEM_URL = "https://trackapi.nutritionix.com/v2/search/item"

engine = pyttsx3.init()

while True:

    food_input = input("What branded food would you like information on? (or type 'exit') ")

    if food_input.lower() == "exit":
        break

    try:
        search_params = {
            "query": food_input,
            "branded": True
        }
        search_response = requests.get(SEARCH_URL, headers=HEADERS, params=search_params)
        search_response.raise_for_status()
        search_result = search_response.json()

        if not search_result['branded']:
            print("No branded item found under the name '"+ str(food_input) + "'. Try being more specific.")
            engine.say("No branded item found under the name '"+ str(food_input) + "'. Try being more specific.")
            engine.runAndWait()
            continue

        branded_item = search_result['branded'][0]
        item_id = branded_item['nix_item_id']

        item_params = {"nix_item_id": item_id}
        item_response = requests.get(ITEM_URL, headers=HEADERS, params=item_params)
        item_response.raise_for_status()
        item = item_response.json()['foods'][0]

        print(f"\n--- Nutrition Info for: {item['food_name']} ---")
        print(f"Brand: {item.get('brand_name', 'N/A')}")
        print(f"Serving: {item['serving_qty']} {item['serving_unit']} ({item.get('serving_weight_grams', 'N/A')} g)")
        print(f"Calories: {item.get('nf_calories', 'N/A')} kcal")
        print(f"Total Fat: {item.get('nf_total_fat', 'N/A')} g")
        print(f"Sugar: {item.get('nf_sugars', 'N/A')} g")
        print(f"Cholesterol: {item.get('nf_cholesterol', 'N/A')} mg")
        print(f"Sodium: {item.get('nf_sodium', 'N/A')} mg")
        print(f"Carbohydrates: {item.get('nf_total_carbohydrate', 'N/A')} g")
        print(f"Protein: {item.get('nf_protein', 'N/A')} g\n")
        voices = engine.getProperty('voices')
        #print(str(voices))

        engine.setProperty('voice', voices[0].id)

        engine.say(str(item.get('brand_name')) + "'s " + str(item['food_name']) + "has " + str(item.get('nf_calories')) + " Calories in a single serving.")
        engine.runAndWait()

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        engine.say(f"Network error: {e}")
        engine.runAndWait()
    except (KeyError, IndexError) as e:
        print("Unexpected API response format or missing data.")
        engine.say("Unexpected API response format or missing data.")
        engine.runAndWait()
