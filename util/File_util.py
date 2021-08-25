import os
import time
from util.Config_loader import Config_loader
from PIL import Image

class File_util():
    year=time.strftime("%Y", time.localtime())
    month=time.strftime("%m", time.localtime())
    day=time.strftime("%d", time.localtime())
    root_path=""
    path_delimiter=""

    def __init__(self):
        self.path_delimiter=os.sep
        loader=Config_loader()
        base_path=loader.get_root_path()
        if base_path.__contains__("\\") and base_path.__contains__("/"):
            raise Exception("请检查config.yaml文件中的路径配置是否正确")
        elif base_path[-1]=="\\" or base_path[-1]=="/":
            self.root_path=base_path
            # print(self.root_path)
        elif base_path.__contains__("\\"):
            self.root_path=base_path+"\\"
            # print(self.root_path)
        elif base_path.__contains__("/"):
            self.root_path=base_path+"/"
            # print(self.root_path)


    def save_image(self,file_name,file):
        abs_path=self.root_path + self.year + self.path_delimiter + self.month + self.path_delimiter + self.day
        path = abs_path+ self.path_delimiter+ file_name # 图片路径
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
        img = Image.open(file)
        img.save(path)

    def get_path(self,file_name):
        abs_path = self.root_path + self.year + self.path_delimiter + self.month + self.path_delimiter + self.day
        path = abs_path + self.path_delimiter + file_name  # 图片路径
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)
        return path

    # def get_date(self):
    #     return (self.year,self.month,self.day)
