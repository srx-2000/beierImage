# import pymysql
from db.db_client import db_client
from util.Config_loader import Config_loader

loader=Config_loader()
print(loader.get_server_host())
print(loader.get_server_port())


db_client=db_client()
# db_client.init_db()
# db_client.insert_single_image("64304942_p0_master1200.jpg","e3618c63cc7c0801db76d5589468f6db","http://localhost:5000/show/e3618c63cc7c0801db76d5589468f6db.jpg",
#                               "D:\\image_bed\\2021\\08\\25","2021","08","25")

db_client.select_single_image_by_id("e3618c63cc7c0801db76d5589468f6db")
data=db_client.select_single_image_by_date("2021")
print(len(data) == 0)
print(data)

print(db_client.query_count())
print(list(db_client.select_single_image_by_date(None)))
# db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='srx62600', db='image_database', charset='utf8')
#
# cursor = db.cursor()
# cursor.execute("select version()")
# data = cursor.fetchone()
# print(data)
#

