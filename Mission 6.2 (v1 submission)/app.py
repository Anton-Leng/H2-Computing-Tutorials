from flask import Flask, render_template, url_for, redirect, request
import os.path
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        TableNo = request.form["TableNo"]

        query = """
        INSERT INTO Customer (TableNo)
        VALUES (?)
        """

        db = sqlite3.connect("stall.db")
        db.execute(query, (TableNo,))
        db.commit()
        db.close()

        query1 = """
        SELECT CustID
        FROM Customer
        WHERE TableNo = ?
        """

        conn = sqlite3.connect("stall.db")
        cursor = conn.execute(query1, (TableNo,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template('endRegister.html', data=data)

@app.route("/order/", methods=["GET", "POST"])
def order():
    if request.method == "GET":
        query = """
        SELECT * 
        FROM Item
        """

        db = sqlite3.connect("stall.db")
        cursor = db.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()

        rice = []
        noodles = []
        sides = []
        bev = []
        dessert = []

        for item in data:
            if "R" in item[0]:
                rice.append(item)
            elif "N" in item[0]:
                noodles.append(item)
            elif "S" in item[0]:
                sides.append(item)
            elif "B" in item[0]:
                bev.append(item)
            elif "D" in item[0]:
                dessert.append(item)

        return render_template("order.html", rice=rice, noodles=noodles, sides=sides, bev=bev, dessert=dessert)

    else:
        OrderChoice = request.form["OrderChoice"]
        qty = request.form["qty"]
        remarks = request.form["remarks"]
        custID = request.form["custID"]

        query2 = """
        INSERT INTO Orders (ItemID, Remarks, CustID, Quantity)
        VALUES (?, ?, ?, ?)
        """

        db = sqlite3.connect("stall.db")
        db.execute(query2, (OrderChoice, remarks, custID, qty))
        db.commit()
        db.close()

        return "Your order has been processed. Please wait for your meal."

@app.route('/viewBillcust/', methods=["GET", "POST"])
def viewBillcust():
    if request.method == "GET":
        return render_template("billCust.html")
    else:
        custID = request.form["custID"]

        query3 = """
        SELECT Item.Name, Orders.Quantity, Item.Price
        FROM Orders, Item
        WHERE Orders.CustID = ?
        AND Orders.ItemID = Item.ItemID
        """

        db = sqlite3.connect("stall.db")
        cursor = db.execute(query3, (custID,))
        data = cursor.fetchall()
        cursor.close()
        db.close()

        total = 0

        for ele in data:
            total += (ele[1] * ele[2])

        return render_template("billDisplayCust.html", data=data, total=total)

@app.route('/staff/', methods=["GET", "POST"])
def staff():
    if request.method == "GET":
        return render_template("staff.html")
    else:
        pwd = request.form["pwd"]

        if pwd == "M1804C":
            return render_template("staff_opt.html")
        else:
            return "Wrong staff password provided. Do not enter if you're not a staff member. Thank you."

@app.route('/addItem/', methods=["GET", "POST"])
def addItem():
    if request.method == "GET":
        return render_template("addItem.html")
    else:
        itemID = request.form["itemID"]
        itemName = request.form["itemName"]
        itemPx = request.form["itemPx"]
        itemPic = request.files["itemPic"]


        new_pic_link = "static/items/" + itemPic.filename

        itemPic.save(new_pic_link)

        query5 = """
        INSERT INTO Item
        VALUES (?, ?, ?, ?)
        """

        db = sqlite3.connect("stall.db")
        db.execute(query5, (itemID, itemName, itemPx, new_pic_link))
        db.commit()
        db.close()

        return "Item has been added to menu." 

@app.route('/updateItem/', methods=["GET", "POST"])
def updateItem():
    if request.method == "GET":
        return render_template("updateItem.html")
    else:
        updateField = request.form["updateField"]

        if updateField == "ItemID":
            return render_template("updateID.html")
        elif updateField == "Name":
            return render_template("updateName.html")
        elif updateField == "Price":
            return render_template("updatePx.html")
        else:
            return render_template("updatePic.html")


@app.route('/updateItemID/', methods=["GET", "POST"])
def updateItemID():
    if request.method == "GET":
        return render_template("updateID.html")
    else:
        itemID = request.form["itemID"]
        itemDetail = request.form["itemDetail"]

        query6 = """
        UPDATE Item 
        SET ItemID = ?
        WHERE ItemID = ?
        """

        db = sqlite3.connect("stall.db")
        db.execute(query6, (itemDetail, itemID))
        db.commit()
        db.close()

        return "Item has been updated." 

@app.route('/updateItemName/', methods=["GET", "POST"])
def updateItemName():
    if request.method == "GET":
        return render_template("updateName.html")
    else:
        itemID = request.form["itemID"]
        itemDetail = request.form["itemDetail"]

        query6 = """
        UPDATE Item 
        SET Name = ?
        WHERE ItemID = ?
        """

        db = sqlite3.connect("stall.db")
        db.execute(query6, (itemDetail, itemID))
        db.commit()
        db.close()

        return "Item has been updated." 

@app.route('/updateItemPx/', methods=["GET", "POST"])
def updateItemPx():
    if request.method == "GET":
        return render_template("updatePx.html")
    else:
        itemID = request.form["itemID"]
        itemDetail = request.form["itemDetail"]

        query6 = """
        UPDATE Item 
        SET Price = ?
        WHERE ItemID = ?
        """

        db = sqlite3.connect("stall.db")
        db.execute(query6, (itemDetail, itemID))
        db.commit()
        db.close()

        return "Item has been updated." 

@app.route('/updateItemPic/', methods=["GET", "POST"])
def updateItemPic():
    if request.method == "GET":
        return render_template("updatePic.html")
    else:
        itemID = request.form["itemID"]
        itemDetail = request.files["itemDetail"]

        new_pic_link = "static/items/" + itemDetail.filename

        itemDetail.save(new_pic_link)

        query6 = """
        UPDATE Item 
        SET Picture = ?
        WHERE ItemID = ?
        """

        db = sqlite3.connect("stall.db")
        db.execute(query6, (new_pic_link, itemID))
        db.commit()
        db.close()

        return "Item has been updated." 

@app.route('/deleteItem/', methods=["GET", "POST"])
def deleteItem():
    if request.method == "GET":

        query = """
        SELECT * FROM Item
        """

        db = sqlite3.connect("stall.db")
        cursor = db.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()

        return render_template("deleteItem.html", data=data)
    else:
        itemID = request.form['itemID']

        query7 = """
        DELETE FROM Item
        WHERE ItemID = ?
        """

        db = sqlite3.connect("stall.db")
        db.execute(query7, (itemID,))
        db.commit()
        db.close()

        return "Item has been deleted."

@app.route('/deleteCust/', methods=["GET", "POST"])
def deleteCust():
    if request.method == "GET":

        query = """
        SELECT * FROM Customer
        """

        db = sqlite3.connect("stall.db")
        cursor = db.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()

        return render_template("deleteCust.html", data=data)
    else:
        custID = request.form['custID']

        query8 = """
        DELETE FROM Customer
        WHERE CustID = ?
        """

        db = sqlite3.connect("stall.db")
        db.execute(query8, (custID,))
        db.commit()
        db.close()

        return "Customer record has been deleted."

@app.route('/deleteOrder/', methods=["GET", "POST"])
def deleteOrder():
    if request.method == "GET":

        query = """
        SELECT * FROM Orders
        """

        db = sqlite3.connect("stall.db")
        cursor = db.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()

        return render_template("deleteOrder.html", data=data)
    else:
        orderNo = request.form['orderNo']

        query9 = """
        DELETE FROM Orders
        WHERE OrderNo = ?
        """

        db = sqlite3.connect("stall.db")
        db.execute(query9, (orderNo,))
        db.commit()
        db.close()

        return "Order has been deleted."

@app.route('/viewOrder/')
def viewOrder():

    query10 = """
    SELECT Orders.OrderNo, Item.Name, Orders.Remarks, Customer.TableNo
    FROM Orders, Item, Customer
    WHERE Orders.CustID = Customer.CustID
    AND Orders.ItemID = Item.ItemID
    """

    db = sqlite3.connect("stall.db")
    cursor = db.execute(query10)
    data = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("viewOrder.html", data=data)

@app.route('/viewBill/', methods=["GET", "POST"])
def viewBill():
    if request.method == "GET":
        return render_template("billStaff.html")
    else:
        custID = request.form["custID"]

        query4 = """
        SELECT Item.Name, Orders.Quantity, Item.Price
        FROM Orders, Item, Customer
        WHERE Orders.CustID = ?
        AND Orders.ItemID = Item.ItemID
        AND Orders.CustID = Customer.CustID
        """

        db = sqlite3.connect("stall.db")
        cursor = db.execute(query4, (custID,))
        data = cursor.fetchall()
        cursor.close()
        db.close()

        total = 0

        for ele in data:
            total += (ele[1] * ele[2])

        return render_template("billDisplayStaff.html", data=data, total=total)

if __name__ == "__main__":
    app.run(port=5008, debug=True)