from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return "My Homepage"

@app.route('/search/', methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        customer_id = request.form["customer_id"]
#        query = """
#        SELECT Policies.PolicyID, Policies.YearlyPremium, Policies.TotalYears, Policies.ProtectedSum
#        FROM Policies, PolicyRecords
#        WHERE Policies.PolicyID == PolicyRecords.PolicyID
#        AND PolicyRecords.CustomerID = ?
#        ORDER BY PolicyRecords.StartDate
#        """
        query = query = """
        SELECT *
        FROM PolicyRecords
        WHERE CustomerID = ?
        ORDER BY StartDate
        """


        db = sqlite3.connect("Tutorial web app 01 (Task 1.2).db")
        cursor = db.execute(query, (customer_id,))
        data = cursor.fetchall()
        cursor.close()
        db.close()
    
        return render_template("display.html", data=data)
        
@app.route('/policy_details/<policy_id>')
def policy_details(policy_id):
    query = """
    SELECT * FROM Policies
    WHERE PolicyID = ?
    """

    db = sqlite3.connect("Tutorial web app 01 (Task 1.2).db")
    cursor = db.execute(query, (policy_id,))
    data = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("policy_detail.html", data=data)

if __name__ == "__main__":
    app.run(debug=True) # for exam, use debug=False