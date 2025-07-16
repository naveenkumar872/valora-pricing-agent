from flask import Flask, render_template, request
from backend.trainer import run_pricing_simulation

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form["query"]
        base_cost = int(request.form["base_cost"])
        rounds = int(request.form.get("rounds", 5))

        result = run_pricing_simulation(query, rounds, base_cost)

        return render_template("index.html", result=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
