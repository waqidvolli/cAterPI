from flask import Flask, request, jsonify, abort
from flask.ext.cors import CORS
from flask_mail import Mail, Message
from dbconnect import connection

application = Flask(__name__)
application.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = '<REPLACE-WITH-EMAIL_ID>',
    MAIL_PASSWORD = "<REPLACE-WITH-PASSWORD>"
    )

mail=Mail(application)
#Cross-Origin Resource Sharing application
CORS(application)

#By default, there is atleast 1 order in local memory.
orders = [{
      "address": "6 Metrotech, NYU",
      "cuisine": "Italian",
      "email": "wmv214@nyu.edu",
      "id": 1,
      "name": "Waqid Munawar",
      "people": 5,
      "phone": "917-960-2468"
    }];


@application.route('/')
def index():
    html = '''
    <p><h1>Welcome to cAterPI - The API for your catering requirements!!</h1></p>
    <hr>
    <p><h3>1) To fetch the list of orders:</h3></p>
    Append the URL with: <b><code>/caterpi/v1.0/orders</code></b> to fetch the list of orders that is returned as a JSON object.</p>
    <p>eg: If you are <u>running on your local system</u>, the URL will be <b><code>http://localhost:5000/caterpi/v1.0/orders</code></b>
    <p><u>If you are running it on AWS</u>, the URL will be <b><code>http://caterpi-dev.us-west-2.elasticbeanstalk.com/caterpi/v1.0/orders</code></b>
    <p>Sample Response:<pre><code>
    {
      "orders": [
        {
          "address": "6 Metrotech, NYU",
          "cuisine": "Italian",
          "email": "wmv214@nyu.edu",
          "id": 1,
          "name": "Waqid Munawar",
          "people": 5,
          "phone": "917-960-2468"
        }
      ]
    }
    </code></pre></p>
    <br>
    <hr>
    <p><h3>2) To submit a new order, you have to make a POST request to the above URL's (local/AWS)</h3></p>
    <p>eg: <u>To test on local</u>, you can open a new terminal (in MAC) and type the following:</p>
    <p><b><code>curl -i -H "Content-Type: application/json" -X POST -d '{"address": "2 Metrotech","cuisine": "Chinese","email": "n123@nyu.edu",
    "name": "New Test User","people": 5, "phone": "917-960-2468"}' http://localhost:5000/caterpi/v1.0/orders</code></b></p>
    <p>Sample Response:<pre><code>
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 275
    Server: Werkzeug/0.11.5 Python/2.7.11
    Date: Fri, 08 Apr 2016 16:33:49 GMT

    {
      "msg": "We have received your request and will get back to you shortly!",
      "order": {
        "address": "2 Metrotech",
        "cuisine": "Chinese",
        "email": "n123@nyu.edu",
        "id": 3,
        "name": "New Test User",
        "people": 5,
        "phone": "917-960-2468"
      }
    }
    </code></pre></p>
    <p>eg: <u>To test on AWS</u>, you can use the following snippet on your front end OR from browser:</p>
    <pre><code>

    var url = "http://caterpi-dev.us-west-2.elasticbeanstalk.com/caterpi/v1.0/orders";
    var jsonData = {"address": "2 Metrotech","cuisine": "Chinese","email": "n123@nyu.edu", "name": "New Test User","people": 5, "phone": "917-960-2468"};
    var requestStr = JSON.stringify(jsonData);
    $.ajax({
        type: "POST",
        url: url,
        data: requestStr,
        contentType: "application/json"
    }).done(function(response) {
        alert(JSON.stringify(response));
        console.log(JSON.stringify(response));
    });
    </code></pre>
    <p>Alternatively, as of April 8, 2016 12:45pm, there is a fron end form hosted at <b><code>http://ec2-52-88-241-24.us-west-2.compute.amazonaws.com/caterpi/</code></b> which you can use to submit a new order request.</p>
    <hr>
    '''
    return html

#API to fetch list of all orders
@application.route('/caterpi/v1.0/orders', methods=['GET'])
def get_tasks():
    c, conn = connection()
    sql = "SELECT * FROM orders"
    c.execute(sql)
    data = c.fetchall()
    
    for row in data:
        order = {
            'id': row[0],
            'name': row[1],
            'phone': row[2],
            'email': row[3],
            'people': row[4],
            'address': row[6],
            'cuisine': row[5]
        }
        orders.append(order)
        
    return jsonify({'orders': orders})

#API to submit a new order
@application.route('/caterpi/v1.0/orders', methods=['POST'])
def create_task():
    if not request.json: #or not 'phone' in request.json:
        abort(400)

    name = request.json.get('name', "")
    phone = request.json['phone']
    email = request.json.get('email',"")
    people = request.json.get('people',"")
    address = request.json.get('address',"")
    cuisine = request.json.get('cuisine',"")
    
    c, conn = connection()
    sql = "INSERT INTO orders (name, phone, email, people, cuisine, address) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (name, phone, email, people, cuisine, address)
    c.execute(sql)
    conn.commit()
    sql = "SELECT id FROM orders ORDER BY id DESC LIMIT 1"
    c.execute(sql)

    # Retrieve newest data ID, display in retured json obj
    data = c.fetchall()
    for row in data:
        id = row[0]

    c.close()
    conn.close()

    order = {
        'id': id,
        'name': name,
        'phone': phone,
        'email': email,
        'people': people,
        'address': address,
        'cuisine': cuisine
    }
    msg = Message('Order Confirmation',sender='teamcaterpi@dgoogle.com',recipients=[email])
    msg.body = "Thank you. We have received your request and will get back to you shortly! "
    mail.send(msg)
    return jsonify({'msg': 'We have received your request and will get back to you shortly!', 'order': order}), 201


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
