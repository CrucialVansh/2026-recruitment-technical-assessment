from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = None

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	# TODO: implement me
	whitespace = re.compile(r'[-_\s]+')
	recipeName = whitespace.sub(" ", recipeName)
	rm_spec_char = re.compile(r'[^a-zA-Z\s]')
	recipeName = rm_spec_char.sub('', recipeName)

	if not recipeName:
		return None
	else:
		return recipeName.title().strip()


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook

# Assuming saving means to save in memory, I'm gonna use a global variable
cookbook: Dict[str, CookbookEntry] = {}

@app.route('/entry', methods=['POST'])
def create_entry():
	# TODO: implement me
	data = request.get_json()
	name = data.get("name")
	entry_type = data.get("type")

	if name in cookbook:
		return 'Name already exists', 400

	if entry_type == "ingredient":
		cook_time = data.get("cookTime")
		if cook_time is None or cook_time < 0:
			return 'Invalid cookTime', 400

		cookbook[name] = Ingredient(name=name, cook_time=cook_time)

	elif entry_type == "recipe":
		required_items = data.get("requiredItems", [])

		item_names = [item["name"] for item in required_items]
		if len(item_names) != len(set(item_names)):
			return 'Duplicate items in recipe', 400

		items_list = [RequiredItem(name=i["name"], quantity=i["quantity"]) for i in required_items]
		cookbook[name] = Recipe(name=name, required_items=items_list)

	else:
		return 'Invalid type', 400

	return '', 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
