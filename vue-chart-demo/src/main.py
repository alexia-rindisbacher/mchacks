from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Physical_Waste():
    item_weights = {
        "Pen": 0.02,
        "Shirt": 0.17,
        "Sticker": 0.002,
        "Brochure": 0.018,
        "Lanyard": 0.025,
        "Tote": 0.15
    }

    # Environmental impact per kg for each material
    materials_db = {
        "Plastic": {
            "co2": 2.10, # kg CO2 per kg
            "water": 0.198, # EIP (Environmental Impact Points) per kg
            "energy": 622.0, # EIP per kg
            "gwi": 2110.0
        },
        "Metal": {
            "co2": 8.89,
            "water": 36.2,
            "energy": 1280.0,
            "gwi": 8880.0
        },
        "Biodegradable": {
            "co2": 2.70,
            "water": 2.97,
            "energy": 451.0,
            "gwi": 2710.0
        },
        "Synthetic Fabric": {
            "co2": 2.80,
            "water": 1.02,
            "energy": 600.0,
            "gwi": 2810.0
        },
        "Cotton Fiber": {
            "co2": 2.94,
            "water": 149.0,
            "energy": 331.0,
            "gwi": 2950.0
        },
        "Paper": {
            "co2": 0.701,
            "water": 5.73,
            "energy": 244.0,
            "gwi": 737.0
        }
    }


def calculate_physical_impact(item, quantity=1):
    item_lower = item.lower()

    if "plastic" in item_lower:
        material = "Plastic"
    elif "metal" in item_lower:
        material = "Metal"
    elif "biodegradable" in item_lower:
        material = "Biodegradable"
    elif "synthetic" in item_lower:
        material = "Synthetic Fabric"
    elif "cotton" in item_lower:
        material = "Cotton Fiber"
    elif "paper" in item_lower:
        material = "Paper"
    else:
        raise ValueError(f"Could not determine material from item: {item}")

    # Access class variables correctly
    base_item = item.split()[0]
    if base_item not in Physical_Waste.item_weights:
        raise ValueError(f"Unknown item: {item}")
    if material not in Physical_Waste.materials_db:
        raise ValueError(f"Unknown material: {material}")

    weight = Physical_Waste.item_weights[base_item]
    mat_data = Physical_Waste.materials_db[material]

    # Calculate impacts
    total_co2 = quantity * weight * mat_data["co2"]
    total_water = quantity * weight * mat_data["water"]
    total_energy = quantity * weight * mat_data["energy"]
    total_gwi = quantity * weight * mat_data["gwi"]

    return total_co2, total_water, total_energy, total_gwi

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    if not data or "item" not in data:
        return jsonify({"error": "Please provide an 'item' field in JSON"}), 400

    item = data["item"]
    quantity = data.get("quantity", 1)

    try:
        quantity = float(quantity)
        total_co2, total_water, total_energy, total_gwi = calculate_physical_impact(item, quantity)
        return jsonify(
            total_co2=total_co2,
            total_water=total_water,
            total_energy=total_energy,
            total_gwi=total_gwi
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


class Travel():
    trans_mode = {
        "Car": {
            "co2": 0.17, # kg CO2 per pkm
            "water": 5, # EIP per pkm
            "energy": 80, # EIP per pkm
            "gwi": 90, # EIP per pkm
        },
        "Bus": {
            "co2": 0.08,
            "water": 2,
            "energy": 35,
            "gwi": 40,
        },
        "Train": {
            "co2": 0.01,
            "water": 0.5,
            "energy": 10,
            "gwi": 12,
        },
        "Plane": {
            "co2": 0.15,
            "water": 3,
            "energy": 90,
            "gwi": 100,
        }
    }

def calculate_travel_impact(mode, dist, participants):
    data = Travel.trans_mode.get(mode)
    if data is None:
        raise ValueError("Unknown transportation mode")
    co2 = data["co2"] * dist * participants
    water = data["water"] * dist * participants
    energy = data["energy"]* dist * participants
    gwi = data["gwi"] * dist * participants
    return co2, water, energy, gwi

@app.route("/travel", methods=["POST"])
def travel():
    data = request.get_json()
    mode = data.get("mode")
    dist = float(data.get("distance", 0))
    participants = float(data.get("participants", 1))

    try:
        co2, water, energy, gwi = calculate_travel_impact(mode, dist, participants)
        return jsonify(
            total_co2=co2,
            total_water=water,
            total_energy=energy,
            total_gwi=gwi
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


class Technology:
    tech_waste = {
        "AI Prompts": {
            "co2": 0.0025,
            "water": 0.015,
            "energy": 0.12,
            "gwi": 0.45
        },
        "Personal Device": {
            "co2": 0.02,
            "water": 1.2,
            "energy": 4.0,
            "gwi": 15.0
        },
        "Large Device": {
            "co2": 0.1,
            "water": 6.0,
            "energy": 20.0,
            "gwi": 75.0
        }
    }

    @staticmethod
    def calculate_tech(type, num, participants):
        if type not in Technology.tech_waste:
            raise ValueError(f"Unknown technology type: {type}")

        data = Technology.tech_waste[type]

        total_co2 = data["co2"] * num * participants
        total_water = data["water"] * num * participants
        total_energy = data["energy"] * num * participants
        total_gwi = data["gwi"] * num * participants

        return total_co2, total_water, total_energy, total_gwi

@app.route("/technology", methods=["POST"])
def technology():
    data = request.get_json()

    try:
        tech_type = data["type"]
        num = float(data.get("num", 1))
        participants = float(data.get("participants", 1))  # new

        total_co2, total_water, total_energy, total_gwi = (
            Technology.calculate_tech(tech_type, num, participants)
        )

        return jsonify(
            total_co2=total_co2,
            total_water=total_water,
            total_energy=total_energy,
            total_gwi=total_gwi
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


class Food:
    packaging_waste = {
        "Reusable": {"co2": 0, "water": 0, "energy": 0, "gwi": 0}, # per 0.15 kg package
        "Compostable": {"co2": 0.06, "water": 0.0446, "energy": 11, "gwi": 40},
        "Paper": {"co2": 0.11, "water": 0.86, "energy": 36.6, "gwi": 110.55},
        "Plastic": {"co2": 0.315,
    "water": 0.03,
    "energy": 93.3,
    "gwi": 316.5}
    }

    diet = {
        "Plant-Based": {"co2": 0.5, "water": 0.6, "energy": 70, "gwi": 400},
        "Meat": {"co2": 2.5, "water": 15, "energy": 200, "gwi": 2000}
    }

    @staticmethod
    def calculate_food(packaging_type, diet_type, num=1):
        if packaging_type not in Food.packaging_waste:
            raise ValueError(f"Unknown packaging type: {packaging_type}")
        if diet_type not in Food.diet:
            raise ValueError(f"Unknown diet type: {diet_type}")

        packaging_data = Food.packaging_waste[packaging_type]
        diet_data = Food.diet[diet_type]

        total_co2 = (packaging_data["co2"] + diet_data["co2"]) * num
        total_water = (packaging_data["water"] + diet_data["water"]) * num
        total_energy = (packaging_data["energy"] + diet_data["energy"]) * num
        total_gwi = (packaging_data["gwi"] + diet_data["gwi"]) * num

        return total_co2, total_water, total_energy, total_gwi



@app.route("/food", methods=["POST"])
def food():
    data = request.get_json()
    try:
        total_co2, total_water, total_energy, total_gwi = Food.calculate_food(
            data["packaging"], data["diet"], float(data.get("num", 1))
        )
        return jsonify(total_co2=total_co2, total_water=total_water,
                       total_energy=total_energy, total_gwi=total_gwi)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


class Total():
    # 2026 Recommended Weights
    WEIGHTS = {
        "co2": 0.40,    # Carbon Dioxide Emissions Weighted Most Heavily
        "gwi": 0.25,    # Global Warming Impact (non-CO2)
        "energy": 0.20, # Resource Efficiency
        "water": 0.15   # Local Resource Stress
    }

    @staticmethod
    def add_impacts(pw, tr, te, fo):
        """
        Adds impacts from Physical Waste (pw), Travel (tr),
        Technology (te), and Food (fo).
        Each argument should be a tuple or list: (co2, water, energy, gwi)
        """
        total_co2 = pw[0] + tr[0] + te[0] + fo[0]
        total_water = pw[1] + tr[1] + te[1] + fo[1]
        total_energy = pw[2] + tr[2] + te[2] + fo[2]
        total_gwi = pw[3] + tr[3] + te[3] + fo[3]

        return total_co2, total_water, total_energy, total_gwi

    @staticmethod
    def calculate_event_sustainability_score(num_participants, hours, impacts):
        """
        impacts: tuple of (total_co2, total_water, total_energy, total_gwi)
        returns: A dictionary with the normalized score and 2026 rating.
        """
        t_co2, t_water, t_energy, t_gwi = impacts

        # 1. Calculate Weighted Impact Score (WIS)
        # Using the formula: (Metric * Weight)
        weighted_sum = (
            (t_co2 * Total.WEIGHTS["co2"]) +
            (t_gwi * Total.WEIGHTS["gwi"]) +
            (t_energy * Total.WEIGHTS["energy"]) +
            (t_water * Total.WEIGHTS["water"])
        )

        # 2. Normalize by Participant-Hours
        person_hours = num_participants * hours
        if person_hours == 0:
            return {"error": "Duration or participants cannot be zero"}

        final_score = weighted_sum / person_hours

        # 3. Determine 2026 "Good Job" Rating
        # Thresholds based on 2026 benchmarks (Weighted units per participant-hour)
        #
        if final_score < 100:
            rating = "Platinum (Excellent)"
        elif final_score <= 150:
            rating = "Green (Good Job)"
        else:
            rating = "High Impact (Needs Optimization)"

        return {
            "sustainability_score": round(final_score, 2),
            "rating": rating,
            "total_person_hours": person_hours,
            "breakdown": {
                "total_co2_kg": round(t_co2, 2),
                "total_eip_energy": round(t_energy, 2),
                "total_eip_water": round(t_water, 2),
                "total_eip_gwi": round(t_gwi, 2)
            }
        }

@app.route("/total", methods=["POST"])
def total():
    data = request.get_json()

    try:
        pw = tuple(data["physical_waste"])
        tr = tuple(data["travel"])
        te = tuple(data["technology"])
        fo = tuple(data["food"])

        participants = float(data["participants"])
        hours = float(data["hours"])

        totals = Total.add_impacts(pw, tr, te, fo)

        result = Total.calculate_event_sustainability_score(
            participants, hours, totals
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')
