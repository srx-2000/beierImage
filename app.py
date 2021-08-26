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

from flask import Response, Flask,request,jsonify,send_from_directory
from util.File_util import File_util
from util.Code_util import Code_util
from db.db_client import db_client
from util.Config_loader import Config_loader
import os


app = Flask(__name__)
client=db_client()
client.init_db()
loader=Config_loader()

api_list = [
    {"url": "/upload","method":"post","params": "image:file", "desc": "上传一个图片【upload single image】"},
    {"url": "/show", "method":"get","params": "/image_uuid", "desc": "在线浏览一个图片【show single image】"},
    {"url": "/all", "method":"get","params": "", "desc": "返回所有图片的信息【show all image info】"},
    {"url": "/query", "method":"get","params": "/year/month/day", "desc": "根据传入的年月日搜索图片【query image info by date】"},
    {"url": "/download", "method":"get","params": "/image_uuid", "desc": "下载指定图片【download single image】"},
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
            return jsonify({"image_name":img.filename,"image_uuid":uuid,"url":"/show/"+uuid,"download_url":"/download/"+uuid,"status":"success"})
        return jsonify({"image_name":img.filename,"status":"fail"})
    else:
        return jsonify({"image_name":img.filename,"status":"fail"})

@app.route('/all',methods=["get"])
def show_all_info():
    count=client.query_count()[0]
    datas=client.select_single_image_by_date(None)
    info_list = []
    for info in datas:
        info_list.append({"image_name": info[1], "image_uuid": info[2], "url": "/show/" + info[2],"download_url":"/download/"+info[2]})
    return jsonify({"info_list":info_list,"all_count":count,"status":"success"})


@app.route('/query/<string:year>/<string:month>/<string:day>',methods=["get"])
@app.route('/query/<string:year>/<string:month>',methods=["get"])
@app.route('/query/<string:year>',methods=["get"])
@app.route('/query',methods=["get"])
def show_info_by_date(year=None,month=None,day=None):
    if year==None:
        return jsonify({"message":"please enter year"})
    datas=client.select_single_image_by_date(year,month,day)
    if len(datas)==0:
        return jsonify({"message":"no find any image info"})
    info_list=[]
    for info in datas:
        info_list.append({"image_name":info[1],"image_uuid":info[2],"url":"/show/"+info[2],"download_url":"/download/"+info[2]})
    return jsonify({"info_list":info_list,"status":"success"})

@app.route("/show/<string:image_id>",methods=["get"])
def show(image_id):
    data=client.select_single_image_by_id(image_id)
    if data!=None:
        imgPath=data[3]
        with open(imgPath, 'rb') as f:
            image = f.read()
        resp = Response(image, mimetype="image/jpeg")
        return resp
    else:
        return jsonify({"message": "not find that image"})

@app.route('/download/<string:imageid>', methods=['GET'])
def download(imageid):
    if request.method == "GET":
        data=client.select_single_image_by_id(imageid)
        if data==None:
            return jsonify({"message":"download fail"})
        if os.path.isfile(data[3]):
            path_delimiter=os.sep
            dir_list = list(data)[3].split(path_delimiter)
            dir = path_delimiter.join(dir_list[0:-1])
            return send_from_directory(dir, dir_list[-1], as_attachment=True)


if __name__ == '__main__':
    app.run(host=loader.get_server_host(),port=loader.get_server_port())
