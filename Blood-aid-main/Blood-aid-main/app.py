from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL 
from flask_session import Session
import yaml,smtplib
from email.mime.text import MIMEText
import os

password=os.environ['GMAIL_TOKENS']
print(password)
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Load database configuration
with open('db.dev.yaml', 'r') as file:
    db = yaml.load(file, Loader=yaml.FullLoader)

# Configure MySQL
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("Username")
        password = request.form.get("password")
        email_address = request.form.get("email")
        phonenumber = request.form.get("phone_number")
        bloodgroup = request.form.get("blood_group")
        dob = request.form.get("dob")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        pincode = request.form.get("pincode")

        session["username"] = username
        session["email"] =  email_address 
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(username, password,email, phone_number, blood_group, dob, address, city, state, pin_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, password,email_address, phonenumber, bloodgroup, dob, address, city, state, pincode))
        mysql.connection.commit()
        cur.close()
        sender_email = "jayadeepreddy452002@gmail.com"
        receiver_email =  session.get("email")
           
        subject = "Bloodaid verification"
        message = "verify here"
        send_email (sender_email,receiver_email,subject,message)
        return redirect("/")

    return render_template("register.html")

def send_email(sender_email,receiver_email,subject,message):
 
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, "roqhyamqtmmvynde")
        server.sendmail(sender_email, receiver_email, msg.as_string())
    

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password, role_id FROM user WHERE username = %s AND password = %s", (username, password))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            session["username"] = username
            session["role_id"] = existing_user[2]

            if existing_user[2] == 1:  #role_id 1 is admin
                return redirect("/blood_stock")
            else:
                return redirect("/donor_form")
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template("login.html")

@app.route("/logout")
def logout():
    session["username"] = None
    session["role_id"] = None
    return redirect("/")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donor_form', methods=['GET', 'POST'])
def donor_form():
    if not session.get("username"):
        return redirect("/login")
    if request.method == 'POST':
        userdetails = request.form
        units = int(userdetails.get('units'))
        disease = userdetails.get('disease')
        donated_date = userdetails.get('donated-date')
        username = session.get("username")

        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id FROM user WHERE username = %s", [username])
        user_id = cur.fetchone()[0]  # Retrieve the actual user_id value
        cur.execute("INSERT INTO donation (user_id, units, disease, donated_date) VALUES (%s, %s, %s, %s)", (user_id, units, disease, donated_date))
        mysql.connection.commit()
        cur.close()
        flash('Donation request successful!', 'success')
        return redirect('/donor_form')

    return render_template('donor_form.html')

@app.route('/donation_requests', methods=['GET'])
def donation_requests():
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    cur.execute("SELECT donation_id,username, blood_group, units, disease, donated_date, phone_number,status FROM user JOIN donation ON user.user_id = donation.user_id")
    donation_requests = cur.fetchall()
    cur.close()
    return render_template('donation_requests.html',donation_requests=donation_requests)

@app.route('/patient_form', methods=['GET', 'POST'])
def patient_form():
    if not session.get("username"):
        return redirect("/login")
    if request.method == 'POST':
        userdetails = request.form
        units = int(userdetails.get('units'))
        reason = userdetails.get('reason')
        requested_date = userdetails.get('Requested date')
        username = session.get("username")

        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id FROM user WHERE username = %s", [username])
        user_id = cur.fetchone()[0]  # Retrieve the actual user_id value
        cur.execute("INSERT INTO patient_request (user_id, units, reason, requested_date) VALUES (%s, %s, %s, %s)", (user_id, units, reason, requested_date))
        mysql.connection.commit()
        cur.close()
        flash('Patient request successful!', 'success')
        return redirect('/patient_form')

    return render_template('patient_form.html')

@app.route('/patient_requests', methods=['GET'])
def patient_requests():
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    cur.execute("SELECT  request_id ,username, blood_group, units, reason, requested_date, phone_number, status,request_id FROM user JOIN patient_request ON user.user_id = patient_request.user_id")
    userdetails = cur.fetchall()
    cur.close()
    return render_template('patient_requests.html', userdetails=userdetails)


@app.route('/reject_patient_request/<request_id>', methods=['POST'])
def reject_patient_request(request_id):
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE patient_request SET status = 'rejected' WHERE request_id = %s", [request_id])
    mysql.connection.commit()
    cur.close()
    flash('Request rejected', 'danger')
    return redirect('/patient_requests')

@app.route('/delete/<donation_id>', methods=['POST'])
def delete(donation_id):
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE donation SET status = 'rejected' WHERE donation_id = %s", [donation_id])
    mysql.connection.commit()
    cur.close()
    flash('Request rejected', 'danger')
    return redirect('/donation_requests')

@app.route('/accept_donor/<donation_id>', methods=['POST'])
def accept_donor(donation_id):
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    # cur.execute("SELECT user_id FROM user WHERE username = %s", [username])
    # user_id = cur.fetchone()[0]  # Retrieve the actual user_id value
    cur.execute("UPDATE donation  SET status = 'accepted' WHERE donation_id = %s", [donation_id])
    cur.execute("SELECT donation.units,user.blood_group,blood_stock.units from donation inner join user on user.user_id = donation.user_id join blood_stock on blood_stock.bloodgroup = user.blood_group where donation_id = %s",[donation_id])
    donor = cur.fetchone()
    blood_group= donor[1]
    units=donor[0]
    if cur.rowcount > 0:
        mysql.connection.commit()
        #Update blood stock (you need to specify how much to add or have a specific variable for it)
        cur.execute("UPDATE blood_stock SET units = units + %s WHERE bloodgroup = %s", (units, blood_group))
        mysql.connection.commit()
        flash('Donation request accepted!', 'success')
    else:
        flash('Donor not found or already accepted!', 'danger')
    
    cur.close() 
    return redirect(url_for('donation_requests'))

@app.route('/accept_patient/<request_id>', methods=['POST'])
def accept_patient(request_id):
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    # cur.execute("SELECT user_id FROM user WHERE username = %s", [username])
    # user_id = cur.fetchone()[0]  # Retrieve the actual user_id value
    cur.execute("UPDATE patient_request  SET status = 'accepted' WHERE request_id = %s", [request_id])
    cur.execute("SELECT patient_request.units,user.blood_group,blood_stock.units from patient_request inner join user on user.user_id = patient_request.user_id join blood_stock on blood_stock.bloodgroup = user.blood_group where request_id = %s",[request_id])
    patient = cur.fetchone()
    # print("existing donation details",donor)
    blood_group= patient[1]
    units=patient[0]
    print(blood_group)
    print(units)
    if cur.rowcount > 0:
        mysql.connection.commit()
        #Update blood stock (you need to specify how much to add or have a specific variable for it)
        cur.execute("UPDATE blood_stock SET units = units - %s WHERE bloodgroup = %s", (units, blood_group))
        mysql.connection.commit()
        flash('Patient request accepted!', 'success')
    else:
        flash('Patient not found or already accepted!', 'danger')
    
    cur.close() 
    return redirect(url_for('donation_requests'))


@app.route('/blood_stock', methods=['GET'])
def blood_stock_view():
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    cur.execute("SELECT bloodgroup, units FROM blood_stock")
    blood_stock = cur.fetchall()
    cur.close()
    blood_stock_dict = {row[0]: row[1] for row in blood_stock}
    return render_template('blood_stock.html', blood_stock=blood_stock_dict)


@app.route('/patient_history', methods=['GET'])
def patient_history():
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, blood_group, units, reason, requested_date, status FROM user JOIN patient_request ON user.user_id = patient_request.user_id")
    patient_history = cur.fetchall()  # Ensure this variable name matches
    cur.close()
    return render_template('patient_history.html', patient_history=patient_history)

@app.route('/donor_history', methods=['GET'])
def donor_history():
    if not session.get("username"):
       return redirect("/login")
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, blood_group, units, disease, donated_date, status FROM user JOIN donation ON user.user_id = donation.user_id")
    donor_history = cur.fetchall()  # Ensure this variable name matches
    cur.close()
    return render_template('donor_history.html', donor_history=donor_history)


@app.route('/userdashboard')
def userdashboard():
    if not session.get("username"):
        return redirect("/login")
    return render_template('userdashboard.html')

@app.route('/admindashboard')
def admindashboard():
    if not session.get("username"):
        return redirect("/login")
    return render_template('admindashboard.html')

@app.route('/view_donations')
def view_donations():
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    username = session.get("username")
    cur.execute("SELECT user_id FROM user WHERE username = %s", [username])
    user_id = cur.fetchone()[0]  # Retrieve the actual user_id value
    cur.execute("SELECT units,disease,donated_date,status from donation where user_id = %s",[user_id])
    view_donations=cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('view_donations.html',view_donations=view_donations)


@app.route('/view_requests')
def view_requests():
    if not session.get("username"):
        return redirect("/login")
    cur = mysql.connection.cursor()
    username = session.get("username")
    cur.execute("SELECT user_id FROM user WHERE username = %s", [username])
    user_id = cur.fetchone()[0]  # Retrieve the actual user_id value
    cur.execute("SELECT units,reason,requested_date,status from patient_request where user_id = %s",[user_id])
    view_requests=cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('view_requests.html',view_requests=view_requests)



    

if __name__ == '__main__':
    # initialize_blood_stock()  # Initialize the blood stock table if needed
    app.run(host='0.0.0.0',debug=True)
