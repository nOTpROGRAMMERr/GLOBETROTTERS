# itinerary.py

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from openai import OpenAI
import anthropic
import re
import mysql.connector

app = Flask(__name__)

app.secret_key = 'your_secret_key'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'lolly',
}
preferences1 = ""


def get_db_connection():
    return mysql.connector.connect(**db_config)


keyid = 'your key'
keySecret = 'your key'
import razorpay

# client = razorpay.Client(auth=(keyid, keySecret))

# data = {
#     "amount": 50000,
#     "currency": "INR",
#     "receipt": "order_rcptid_11",
#     "notes": {
#         "name": uname,
#         "for": "GLOBETROTTERS"
#     }}
#
# payment = client.order.create(data=data)
# # print(payment)
# payment_id = payment['id']
# print(payment_id)
uname = ""
status = 0

u_id = 0


@app.route('/')
def root():
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if session.get('user_id'):
        global uname, status
        sta = status
        print(sta)
        return render_template('land.html', user=uname, data=False, sta=sta)
    return render_template('land.html', data=True, sta=0)

@app.before_request
def check_logged_in():
    if request.endpoint not in ['', 'home', 'login', 'about', 'signup', 'static'] and 'user_id' not in session:
        return redirect(url_for('login'))


@app.route('/payment')
def payment():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    else:
        # User is logged in
        global status
        if status == 1:
            # paid
            return redirect(url_for('itinerary'))
        else:
            # not paid
            global uname
            client = razorpay.Client(auth=(keyid, keySecret))

            data = {
                "amount": 50000,
                "currency": "INR",
                "receipt": "order_rcptid_11",
                "notes": {
                    "name": uname,
                    "for": "GLOBETROTTERS"
                }}

            payment = client.order.create(data=data)
            # print(payment)
            payment_id = payment['id']
            print(payment_id)
            return render_template('app.html', data=payment_id)



@app.route('/success', methods=['GET', 'POST'])
def success():
    global status
    conn = get_db_connection()
    cursor = conn.cursor()
    pro = 1
    sql = "UPDATE users SET paid = %s WHERE id = %s"
    cursor.execute(sql, (pro, status))

    # Commit changes to the database
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return redirect(url_for('itinerary'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        global u_id
        u_id = user['id']

        cursor.execute('SELECT preferences FROM users WHERE username = %s', (username,))
        preferences = cursor.fetchone()
        global preferences1
        preferences1 = preferences

        global status
        temp_id = u_id
        cursor.execute('SELECT paid FROM users WHERE id = %s', (temp_id,))
        pro = cursor.fetchone()
        # print(pro)
        cursor.close()
        conn.close()
        status = pro['paid']
        print(status)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            global uname
            uname = user['username']
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('sql_login.html', error=error)
    return render_template('sql_login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        preferences = request.form['preferences']
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))

        if cursor.fetchone():
            error = 'Username already exists. Please choose a different one.'
            cursor.close()
            conn.close()
            return render_template('sql_signup.html', error=error)
        else:
            if check_password_strength(password) == 1:
                cursor.execute('INSERT INTO users (username, password, email, preferences) VALUES (%s, %s, %s, %s)',
                               (username, hashed_password, email, preferences))
                conn.commit()
                cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
                user_id = cursor.fetchone()[0]

                cursor.execute('INSERT INTO sessions (user_id) VALUES (%s)', (user_id,))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('login'))
            else:
                error = check_password_strength(password)
                return render_template('sql_signup.html', error=error)
    return render_template('sql_signup.html')


@app.route('/logout')
def logout():
    global status, u_id, uname
    status = 0
    u_id = 0
    uname = ""
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/itinerary', methods=['GET', 'POST'])
def itinerary():
    if request.method == 'POST':
        location = request.form.get('location')
        from_loc = request.form.get('from_loc')
        cost = request.form.get('cost')
        # no_people = request.form.get('no_people')
        travel_type = request.form.get('travel_type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        preferences = request.form.get('preferences')
        adults = request.form.get('no_adults')
        children = request.form.get('no_children')
        print(adults, children)

        new_prompt = " from " + from_loc + " to " + location + " from " + start_date + " to " + end_date + " of travel with about " + str(
            cost) + (
                         "rs of budget. Also provide break up of cost only if they charge fees somewhere.Number of adult traveller "
                         "for this trip is/are ") + (
                         adults) + "and Number of children traveller " + children + " .Travel_type=" + travel_type + " user preferences = " + str(
            preferences1) + " " + str(
            preferences)

        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a travel agent, skilled man knows the best places in world and advise the best travel itinerary. Always provide content in good structure. Give new day info in new paragraph."},
                {"role": "user", "content": new_prompt}
            ]
        )
        openai_itinerary = completion.choices[0].message.content

        openai_itinerary = re.split('\n', openai_itinerary)

        conn = get_db_connection()
        cursor = conn.cursor()
        global status, u_id
        temp_id = u_id
        cursor.execute('SELECT paid FROM users WHERE id = %s', (temp_id,))
        pro = cursor.fetchone()
        # print(pro[0])
        cursor.close()
        conn.close()
        temp = pro[0]
        status = temp
        if temp == 1:
            client = anthropic.Anthropic(
                your_key="your key",
            )
            prompt = new_prompt
            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.0,
                system="You are a travel agent, skilled man knows the best places in world and advise the best travel itinerary..",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            claude_itinerary = message.content

            claude_itinerary = claude_itinerary[0].text.replace("\n", "<br>")

        else:
            claude_itinerary = "Become a pro traveller by becoming a pro member."

        return render_template('display_itinerary.html', openai_itinerary=openai_itinerary,
                               claude_itinerary=claude_itinerary, proa=temp)

    return render_template('itinerary.html')


@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        # Handle the form submission
        feedback = request.form.get('feedback')
        output_preference = request.form.get('output_preference')

        # Process the feedback and store it in the database
        sql = "INSERT INTO feedback (feedback, output_preference) VALUES (%s, %s)"
        val = (feedback, output_preference)

        # Establish database connection and cursor
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute SQL query
        cursor.execute(sql, val)

        # Commit changes to the database
        conn.commit()

        # Close cursor and connection
        cursor.close()
        conn.close()

        return render_template('feed_sukesh.html')



    elif request.method == 'GET':
        # Render the feedback form
        return render_template('feedback_form.html')


def check_password_strength(password):
    min_length = 8
    uppercase_regex = re.compile(r'[A-Z]')
    lowercase_regex = re.compile(r'[a-z]')
    digit_regex = re.compile(r'\d')
    special_char_regex = re.compile(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]')

    if len(password) < min_length:
        return "Weak: Password should be at least {} characters long".format(min_length)

    # if not uppercase_regex.search(password) or not lowercase_regex.search(password):
    #     return "Weak: Password should contain at least one uppercase and one lowercase letter"
    #
    # if not digit_regex.search(password):
    #     return "Weak: Password should contain at least one digit"

    if not special_char_regex.search(password):
        return "Weak: Password should contain at least one special character"

    return 1


if __name__ == '__main__':
    app.run(debug=True)
