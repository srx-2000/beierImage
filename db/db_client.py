import pymysql
from util.Config_loader import Config_loader

class db_client():
    host=""
    port=""
    db_name=""
    db_username=""
    db_password=""
    loader=Config_loader()
    # db=""
    # cursor=""

    def __init__(self):
        self.host=self.loader.get_db_host()
        self.port=self.loader.get_db_port()
        self.db_name=self.loader.get_db_name()
        self.db_username=self.loader.get_db_username()
        self.db_password=self.loader.get_db_password()

    def __get_connect(self):
        db = pymysql.connect(host=self.host, port=self.port, user=self.db_username, passwd=self.db_password, charset='utf8')
        cursor = db.cursor()
        use_db_sql = "use " + self.db_name
        cursor.execute(use_db_sql)
        return db



    def init_db(self):
        db = pymysql.connect(host=self.host, port=self.port, user=self.db_username, passwd=self.db_password,
                             charset='utf8')
        cursor = db.cursor()
        cursor.execute("drop database if exists "+self.db_name)
        create_db_sql = "create database "+self.db_name
        cursor.execute(create_db_sql)
        use_db_sql="use "+self.db_name
        cursor.execute(use_db_sql)
        cursor.execute("drop table if exists image")
        create_table_sql = """
        CREATE TABLE image (
	        image_id INT PRIMARY KEY AUTO_INCREMENT COMMENT "主键",
	        image_name VARCHAR(255) NOT NULL COMMENT "图片名称",
	        image_uuid VARCHAR(36) NOT NULL COMMENT "图片uuid，由服务端自动生成" ,
	        image_dir VARCHAR(255) NOT NULL COMMENT "图片本地存储地址",
	        `year` INT NOT NULL COMMENT "图片存储年份",
	        `month` INT NOT NULL COMMENT "图片存储月份",
	        `day` INT NOT NULL COMMENT "图片存储日份"
        )
        """
        cursor.execute(create_table_sql)
        db.close()


    def insert_single_image(self,image_name,image_uuid,image_dir,year,month,day):
        db = self.__get_connect()
        cursor = db.cursor()
        sql = "insert into image(image_name,image_uuid,image_dir,`year`,`month`,`day`) values " \
              "('{image_name}','{image_uuid}','{image_dir}','{year}','{month}','{day}')"\
            .format(image_name=image_name,image_uuid=image_uuid,image_dir=image_dir,year=year,month=month,day=day)
        sql=sql.replace("\\","\\\\")
        cursor.execute(sql)
        db.commit()
        data=self.select_single_image_by_id(image_uuid)
        try:
            if data!=None:
                return True
            else:
                return False
        finally:
            db.close()

    def delete_single_image(self,image_id):
        db = self.__get_connect()
        cursor = db.cursor()
        sql = " delete from employee where image_uuid="+image_id
        cursor.execute(sql)
        db.commit()
        # 查看更新后的结果
        data=self.select_single_image_by_id(image_id)
        try:
            if data!=None:
                return True
            else:
                return False
        finally:
            db.close()

    def select_single_image_by_id(self,image_id):
        db = self.__get_connect()
        cursor = db.cursor()
        sql = "select * from image where image_uuid='%s'"%(image_id)
        cursor.execute(sql)
        data = cursor.fetchone()
        db.close()
        return data

    def select_single_image_by_date(self,year=None,month=None,day=None):
        db = self.__get_connect()
        cursor = db.cursor()
        sql = "select * from image"
        try:
            if year!=None:
                sql = sql+" where `year`="+year
                if month!=None:
                    sql=sql+" and `month`="+month
                    if day!=None:
                        sql=sql+" and `day`="+day
                cursor.execute(sql)
                data = cursor.fetchall()
                return data
            else:
                cursor.execute(sql)
                data = cursor.fetchall()
                return data
        finally:
            db.close()

    def query_count(self):
        db = self.__get_connect()
        cursor = db.cursor()
        sql = "select count(*) from image"
        cursor.execute(sql)
        data = cursor.fetchone()
        db.close()
        return data