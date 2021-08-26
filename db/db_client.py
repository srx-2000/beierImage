import pymysql
from util.Config_loader import Config_loader

class db_client():
    host=""
    port=""
    db_name=""
    db_username=""
    db_password=""
    loader=Config_loader()
    db=""
    cursor=""

    def __init__(self):
        self.host=self.loader.get_db_host()
        self.port=self.loader.get_db_port()
        self.db_name=self.loader.get_db_name()
        self.db_username=self.loader.get_db_username()
        self.db_password=self.loader.get_db_password()
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.db_username, passwd=self.db_password, charset='utf8')
        self.cursor = self.db.cursor()


    def init_db(self):
        self.cursor.execute("drop database if exists "+self.db_name)
        create_db_sql = "create database "+self.db_name
        self.cursor.execute(create_db_sql)
        use_db_sql="use "+self.db_name
        self.cursor.execute(use_db_sql)
        self.cursor.execute("drop table if exists image")
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
        self.cursor.execute(create_table_sql)


    def insert_single_image(self,image_name,image_uuid,image_dir,year,month,day):
        use_db_sql = "use " + self.db_name
        self.cursor.execute(use_db_sql)
        sql = "insert into image(image_name,image_uuid,image_dir,`year`,`month`,`day`) values " \
              "('{image_name}','{image_uuid}','{image_dir}','{year}','{month}','{day}')"\
            .format(image_name=image_name,image_uuid=image_uuid,image_dir=image_dir,year=year,month=month,day=day)
        sql=sql.replace("\\","\\\\")
        self.cursor.execute(sql)
        self.db.commit()
        data=self.select_single_image_by_id(image_uuid)
        if data!=None:
            return True
        else:
            return False

    def delete_single_image(self,image_id):
        use_db_sql = "use " + self.db_name
        self.cursor.execute(use_db_sql)
        sql = " delete from employee where image_uuid="+image_id
        self.cursor.execute(sql)
        self.db.commit()
        # 查看更新后的结果
        data=self.select_single_image_by_id(image_id)
        if data!=None:
            return True
        else:
            return False

    def select_single_image_by_id(self,image_id):
        use_db_sql = "use " + self.db_name
        self.cursor.execute(use_db_sql)
        sql = "select * from image where image_uuid='%s'"%(image_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data

    def select_single_image_by_date(self,year=None,month=None,day=None):
        use_db_sql = "use " + self.db_name
        self.cursor.execute(use_db_sql)
        sql = "select * from image"
        if year!=None:
            sql = sql+" where `year`="+year
            if month!=None:
                sql=sql+" and `month`="+month
                if day!=None:
                    sql=sql+" and `day`="+day
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        else:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data

    def query_count(self):
        use_db_sql = "use " + self.db_name
        self.cursor.execute(use_db_sql)
        sql = "select count(*) from image"
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        return data