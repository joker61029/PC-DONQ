from random import seed
import re
from sys import meta_path
from flask import *
import mysql.connector, json
from mysql.connector import errorcode
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import secrets

#uploading image
import logging
import boto3
from botocore.exceptions import ClientError

app=Flask(__name__)
app.secret_key = "(@*&#(283&$(*#"


load_dotenv()
mydb = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_user'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_DATABASE')
)


# Pages
@app.route("/")
def index():
	return render_template("index.html")
    
@app.route("/api/messages", methods=["GET"])
def messages():
    cursor = mydb.cursor(buffered=True)
    sql = "SELECT * FROM message_board.message;"
    cursor.execute(sql)
    mydict = []
    cursor_data = cursor.fetchall()
    for row in cursor_data:
        mydict.append({
            "id": row[0],
            "name": row[1],
            "text": row[2],
            "image": row[3]
        })
    stud_json = json.dumps({"data":mydict}, indent=2, ensure_ascii=False)
    return stud_json, 200


@app.route("/api/messages/<id>", methods=["GET"])
def messages_id(id):
    cursor = mydb.cursor(buffered=True)
    sql = "SELECT * FROM `message` WHERE `id` = %s ;"
    send = (id,)
    cursor.execute(sql, send)
    mydict = []
    for row in cursor:
        mydict.append({
            "id": row[0],
            "name": row[1],
            "text": row[2],
            "image": row[3]
        })
    stud_json = json.dumps({"data":mydict}, indent=2, ensure_ascii=False)
    return stud_json, 200
    


@app.route("/api/message", methods=["GET"])
def message_get():
    if "id" in session:
        cursor = mydb.cursor(buffered=True)
        sql = "SELECT * FROM `message` WHERE `id` = %s ;"
        send = (session["id"][0],)
        cursor.execute(sql, send)
        mydict = []
        for row in cursor:
            mydict.append({
                "id": row[0],
                "name": row[1],
                "text": row[2],
                "image": row[3]
            })
        stud_json = json.dumps({"data":mydict}, indent=2, ensure_ascii=False)
        session.pop("id", None)
        return stud_json
    else:
        return "錯誤執行", 400

@app.route("/api/message", methods=["POST"])
def message_submit():
    name = request.form.get("name")
    text = request.form.get("text")
    if(request.form.get("image_type")=="copy"):
        image_name = "/static/image/copy.jpg"
    else:
        image = request.files.get("image")
        image_type = "."+request.form.get("image_type").split("/")[1]
        image_name = upload_file(image, 'messageboard', image_type)
    cursor = mydb.cursor(buffered=True)
    sql = "INSERT INTO `message` (name, text, image) VALUES (%s,  %s , %s );"
    send  = (name, text, image_name)
    cursor.execute(sql, send)
    mydb.commit()
    sql = "SELECT `id` FROM `message` WHERE `image` = %s "
    send  = (image_name,)
    cursor.execute(sql, send)
    for id in cursor:
        session["id"] = id
    cursor.close()
    stud_json = json.dumps({"ok":True}, indent=2, ensure_ascii=False)
    return stud_json, 200


def upload_file(file_name, bucket, type):
    # Upload the file
    s3_client = boto3.client(
        's3',
        aws_access_key_id = os.getenv('access_key_id'),
        aws_secret_access_key= os.getenv('secret_access_key'),
        )
    new_image_name = secrets.token_hex()
    s3_client.upload_fileobj(file_name, bucket, "donq/"+new_image_name+type, ExtraArgs={'ACL':'public-read'})
    new_image_name = "http://d1a5hxicjbhfyg.cloudfront.net/donq/"+new_image_name+type
    return new_image_name

app.run(port=5000)