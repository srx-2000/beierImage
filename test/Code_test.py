from util.Code_util import Code_util
from util.File_util import File_util
from db.db_client import db_client


import os
# code=Code_util()

# print(code.encode("64304942_p0_master1200.jpg"))
# print(code.encode("你好"))
# print(code.encode("456"))
# print(code.encode("  "))
# file=File_util()
# file.loader()
# f=open("D:\\pycharm\\PyCharm 2020.1.1\\workplace\\image_bed\\64304942_p0_master1200.jpg",mode="rb")
# file.save_image("64304942_p0_master1200.jpg",f)

client=db_client()
data=client.select_single_image_by_id("fa3314847bda0181b6cc13db821de40e")
seq=os.sep
data_list=list(data)[3].split(seq)
str=seq.join(data_list[0:-1])
print(str)



