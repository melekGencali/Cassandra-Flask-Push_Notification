#from marketing_notifications_python.models import app_db
import json
import smtplib
import uuid

from cassandra.cqlengine import connection, columns
from cassandra.cqlengine.connection import cluster
from cassandra.cqlengine.management import sync_table
from flask import Flask, render_template, session, request, flash, jsonify, Response
from werkzeug.datastructures import ImmutableMultiDict

from models.user import Person
from views.api import api
from cassandra.auth import PlainTextAuthProvider
from pywebpush import webpush, WebPushException
import os



from cassandra.cluster import Cluster
auth_provider = PlainTextAuthProvider(
        username='cassandra', password='cassandra')

def cassandra_conn():
    app = Flask(__name__)
    app.register_blueprint(api)

    return app

app=cassandra_conn()


app.config.update(

    #Set the secret key to a sufficiently random value
    SECRET_KEY=os.urandom(24),
    #Set the session cookie to be secure
    SESSION_COOKIE_SECURE=True,
    #Set the session cookie for our app to a unique name
    SESSION_COOKIE_NAME='cassandra-WebSession',
    #Set CSRF tokens to be valid for the duration of the session. This assumes you’re using WTF-CSRF protection
    WTF_CSRF_TIME_LIMIT=None

)


DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH = os.path.join(os.getcwd(),"private_key.txt")
DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH = os.path.join(os.getcwd(),"public_key.txt")

VAPID_PRIVATE_KEY = open(DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH, "r").readline().strip("\n")
VAPID_PUBLIC_KEY = open(DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH, "r").read().strip("\n")

# bu abonelik için birincil iletişim e-postasıdır.
VAPID_CLAIMS = {
"sub": "mailto:mgencali6134@gmail.com"
}


"""def message_to_cql():
     cluster = Cluster()
    session = cluster.connect()
    session.execute("create table flask_Keyspace.eposta(posta_id uuid primary key , email text)")
    session.execute("insert into flask_Keyspace.eposta(email) values(email)")"""



def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS

    )


@app.route('/')
def index():

    return render_template('index.html')

@app.route("/subscription/", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients uses to send around push notification
    """

    if request.method == "GET":
        return Response(response=json.dumps({"public_key": VAPID_PUBLIC_KEY}),
            headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")

    subscription_token = request.get_json("subscription_token")
    return Response(status=201, mimetype="application/json")


@app.route("/email_push/",methods=['POST'])
def email_push():

        email = request.form.get("email")
        print(email)

        #data = json.loads(request.form.get("email"))
        posta = Person.create(email=email)
        posta.save()

        """email = request.form['email']
        print("request form:",request.form)"""

        #item=posta.get_data()
        #return json.dumps({"status": "OK", "email": email})
        return  posta.get_data()


@app.route("/push_v1/",methods=['POST'])
def push_v1():

    message = "size bir bildirimimiz varr :)"
    print("request:",request.data)


    print("is_json",request.is_json)

    if not request.json or not request.json.get('sub_token'):

        return jsonify({'failed':1})

    print("request.json",request.json)

    token = request.json.get('sub_token')
    try:
        token = json.loads(token)
        send_web_push(token, message)


        return jsonify({'success':1})
    except Exception as e:
        print("error",e)
        return jsonify({'failed':str(e)})



if __name__ == '__main__':
    connection.setup(['localhost'], "flask_keyspace", protocol_version=4, retry_connect=True,
                     auth_provider=auth_provider)


    app.debug=True
    app.run()
