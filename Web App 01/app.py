from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def form():
    customer_id = request.form.get("customer_id")

    query = """
    SELECT PolicyID FROM policyrecords
    WHERE CustomerID = ?
    """

    db = sqlite3.connect("Tutorial web app 01 (Task 1.2).db")
    cursor = db.execute(query, (customer_id,))
    data = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("display.html", customer_id=customer_id, data=data)



if __name__ == "__main__":
    app.run(port=5012, debug=True)