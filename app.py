from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}

    if request.method == "POST":
        try:
            cost = float(request.form["cost"])
            price = float(request.form["price"])
            margin_target = float(request.form["margin"]) / 100
            fee_on = request.form.get("fee")

            fee_percent = 0.13 if fee_on else 0

            fee = price * fee_percent
            profit = price - cost - fee
            margin = (profit / price) * 100 if price != 0 else 0

            if (1 - fee_percent - margin_target) > 0:
                recommended = cost / (1 - fee_percent - margin_target)
            else:
                recommended = 0

            result = {
                "profit": round(profit, 2),
                "margin": round(margin, 2),
                "fee": round(fee, 2),
                "recommended": round(recommended, 2),
                "good": profit > 0
            }

        except:
            result = {"error": "Invalid input"}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
