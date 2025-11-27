from flask import Flask, render_template, request
from backend.trainer import run_pricing_simulation
from llm import extract_to_json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get product description and process through LLM
        product_description = request.form["product_description"]
        rounds = int(request.form.get("rounds", 5))
        
        try:
            # Extract structured data from LLM
            extracted_data = extract_to_json(product_description)
            query = extracted_data["product"]
            base_cost = int(extracted_data["base_cost"])
            
            # Run pricing simulation with extracted data
            result = run_pricing_simulation(query, rounds, base_cost)
            return render_template("index.html", result=result)
            
        except Exception as e:
            error_message = f"Error processing input: {str(e)}"
            return render_template("index.html", error=error_message)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
