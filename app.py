# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     app.py
   Description :   接口文件
   Author :        beier
   date：          2021/8/25
-------------------------------------------------
   Change Activity:
                   2021/8/25:
-------------------------------------------------
"""
__author__ = 'beier'

from flask import Response, Flask,request,jsonify
from util.File_util import File_util
from util.Code_util import Code_util
from db.db_client import db_client
from util.Config_loader import Config_loader

app = Flask(__name__)
client=db_client()
client.init_db()
loader=Config_loader()

api_list = [
    {"url": "/upload","method":"post","params": "image:file", "desc": "上传一个图片【upload single image】"},
    {"url": "/show", "method":"get","params": "/image_uuid", "desc": "在线浏览一个图片【show single image】"},
]

@app.route("/")
def index():
    return jsonify({"api_list":api_list})

@app.route('/upload', methods=['post'])
def upload():
    file = File_util()
    code = Code_util()
    img = request.files.get('image')
    if code.encode(img.filename)[1]:
        file_name=img.filename
        image_uuid=code.encode(file_name)[0]
        file_path =file.get_path(image_uuid)
        img.save(file_path)
        uuid=image_uuid.split(".")[0]
        flag=client.insert_single_image(img.filename,uuid,file_path,file.year,file.month,file.day)
        if flag:
            return jsonify({"image_name":img.filename,"image_uuid":uuid,"url":"/show/"+uuid,"status":"success"})
        return jsonify({"image_name":img.filename,"status":"fail"})
    else:
        return jsonify({"image_name":img.filename,"status":"fail"})


@app.route("/show/<string:image_id>",methods=["GET"])
def show(image_id):
    data=client.select_single_image_by_id(image_id)
    if data!=None:
        imgPath=data[3]
        # print(imgPath)
        with open(imgPath, 'rb') as f:
            image = f.read()
        resp = Response(image, mimetype="image/jpeg")
        return resp
    else:
        return jsonify({"message": "not find that image"})

# @app.route('/download/<string:imageid>', methods=['GET'])
# def download(imageid):
#     if request.method == "GET":
#         if os.path.isfile(os.path.join('upload', filename)):
#             return send_from_directory('upload', filename, as_attachment=True)
#         pass


if __name__ == '__main__':
    # print(loader.get_server_port())
    # print(loader.get_server_host())
    app.run(host=loader.get_server_port(),port=loader.get_server_host())
    # app.run(host="127.0.0.1",port="5555")