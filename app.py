from flask import *
import sqlite3

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/edit_values_page', methods = ["POST"])
def edit_values_page():
    return render_template('edit_values_page.html')

@app.route('/query_values_page', methods = ["POST"])
def query_values_page():
    return render_template('query_values_page.html')

@app.route('/addnewmember', methods = ["POST"])
def addnewmember():
    return render_template('membership_page.html')

@app.route('/update', methods = ["POST"])
def update():
    return render_template('update_member_page.html')

@app.route('/transaction', methods = ["POST"])
def transaction():
    return render_template('transaction_page.html')

@app.route('/view_dailyrevenue', methods = ["POST"])
def view_trans():
    return render_template('view_daily_revenue_page.html')

@app.route('/view_monthlyrevenue', methods = ["POST"])
def view_revenue():
    return render_template('view_revenue_page.html')

@app.route('/view_member', methods = ["POST"])
def view_member():
    return render_template('view_member_page.html')

@app.route('/submit_add_member', methods = ["POST"])
def submit_add_member():
    connection = sqlite3.connect("salon DB.db")
    data = request.form
    name = data['name']
    gender = data['gender']
    email = data['email']
    contact = data['contactnumber']
    address = data['address']
    memberid = connection.execute("SELECT seq FROM sqlite_sequence \
WHERE name = 'Members'")
    memberid = int(memberid.fetchall()[0][0])
    memberid += 1
    connection.execute("INSERT INTO Members \
VALUES (?,?,?,?,?,?);",(memberid,name,gender,email,contact,address))
    connection.commit()
    return root()

@app.route('/submit_update_details', methods = ["POST"])
def submit_update_details():
    connection = sqlite3.connect("salon DB.db")
    data = request.form
    memberid = data['memberid']
    email = data['email']
    contact = data['contact number']
    if email!="":
        connection.execute("UPDATE Members \
SET Email = ? \
WHERE id = ?;",(email,memberid))
    if contact!="":
        connection.execute("UPDATE Members \
SET Contact_Number = ? \
WHERE id = ?;",(contact,memberid))
    connection.commit()
    return root()

@app.route('/submit_add_transaction', methods = ["POST"])
def submit_add_transaction():
    connection = sqlite3.connect("salon DB.db")
    data = request.form
    name = data['name']
    memberid = data['memberid']
    date = data['date']
    invoiceid = connection.execute("SELECT seq FROM sqlite_sequence \
WHERE name = 'Transactions'")
    invoiceid = int(invoiceid.fetchall()[0][0])
    invoiceid += 1
    services = []
    prices = []
    total_price = 0.0
    for i in range(1,5):
        index = "s" + str(i)
        temp = data[index]
        if temp != "":
            services.append(temp)
            price = connection.execute("SELECT Price FROM Services_Provided \
WHERE Service = ?", [temp])
            price = float(price.fetchall()[0][0])
            prices.append(price)
            total_price += price
        else:
            break
    if memberid != "0":
        total_price = total_price * 0.9
    total_price = round(total_price,2)
    connection.execute("INSERT INTO Transactions \
VALUES (?,?,?,?,?);",(invoiceid,memberid,name,date,total_price))
    for service in services:
        connection.execute("INSERT INTO Transactionsdetails \
VALUES (?,?);",(invoiceid,service))
    connection.commit()
    return root()

@app.route('/submit_view_transaction', methods = ["POST"])
def submit_view_transaction():
    connection = sqlite3.connect("salon DB.db")
    data = request.form
    date = data['date']
    heading = "Transactions that happened on "+ date
    header = ["Transaction_ID","Member_ID","Name","Date","Total_Payable"]
    data = connection.execute("SELECT * FROM Transactions \
WHERE Date = ?",[date])
    data = data.fetchall()
    return render_template('viewall.html',heading=heading,header=header,data=data)

@app.route('/submit_view_revenue', methods = ["POST"])
def submit_view_revenue():
    connection = sqlite3.connect("salon DB.db")
    data = request.form
    date = data['date']
    heading = "Revenue for "+date
    header = ["Total_Revenue"]
    date = "%"+date
    data = connection.execute("SELECT Payable FROM Transactions \
WHERE Date like ?",[date])
    data = data.fetchall()
    print(data)
    total = 0.0
    for money in data:
        total += float(money[0])
    data = [[total]]
    return render_template('viewall.html',heading=heading,header=header,data=data)


@app.route('/submit_view_member', methods = ["POST"])
def submit_view_member():
    connection = sqlite3.connect("salon DB.db")
    data = request.form
    memberid = data['memberid']
    heading = "Transactions by Memberid:"+memberid
    header = ["Transaction_ID","Member_ID","Name","Date","Total_Payable"]
    data = connection.execute("SELECT * FROM Transactions \
WHERE Member_ID = ?",[memberid])
    data = data.fetchall()
    return render_template('viewall.html',heading=heading,header=header,data=data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
