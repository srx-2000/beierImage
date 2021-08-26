### Beier图床

​	本图床是基于python下的flask框架进行搭建的，目标就是给需要构建自己图床的小伙伴们提供一个简单易懂，开箱即用的轻简图床。由于本人ui水平有限，所以暂时仅提供一些接口供大家clone调用。本项目规模极小，目前仅有不到500行代码，适合新手了解图床的大概情况。

#### 功能（以下功能皆仅提供API）

- [x] **单图片上传**
- [ ] **批量图片上传**
- [x] **在线浏览上传图片**
- [x] **下载单个云端图片**
- [ ] **批量下载云端图片**
- [x] **获取全部图片信息**
- [x] **根据上传时间检索图片**

#### 安装部署

**代码下载**

* git clone

 ```https://github.com/srx-2000/beierImage.git```

**安装依赖**

`pip install -r requirements.txt`

##### 更新配置

```yaml
# 存储根路径
root_path: D:\image_bed
# mysql数据库地址，默认为时本地地址127.0.0.1，如果是要连接远程数据库才需要更改
db_host: 127.0.0.1
# mysql数据库连接端口，默认3306，一般不用改
db_port: 3306
# 数据库名称，默认为image_database
db_name: image_database
# 数据库用户名
db_username: root
# 数据库密码
db_password: 123456
# 服务器host，如果是发布到服务器上就填0.0.0.0，如果是在自己本机上跑都直接默认的127.0.0.1就可以了
server_host: 127.0.0.1
# 服务器port，选择一个自己服务器【本机】上没有被占用的端口即可，默认5555
server_port: 5555
```

 **启动项目**

```python app.py```

**服务器上运行注意事项**

> 1. 记得开启对应端口的防火墙
> 2. 记得将配置文件中的server_host属性改为0.0.0.0
> 3. 使用命令`nohup python app.py > /dev/null &`在后台运行项目
> 4. 如果是跑在linux服务器上，记得改root_path属性
> 5. 数据库密码记得改成自己的

#### 使用

- Api

启动web服务后, 默认配置下会开启 [http://127.0.0.1:5555](http://127.0.0.1:5555/) 的api接口服务

| api       | method | Description              | params                       |
| --------- | ------ | ------------------------ | ---------------------------- |
| /         | GET    | api介绍                  | None                         |
| /upload   | POST   | 上传一张图片             | image:file【form表单提交】   |
| /show     | GET    | 在线浏览一个图片         | /image_uuid【url_param】     |
| /all      | GET    | 返回所有图片的信息       | None                         |
| /query    | GET    | 根据传入的年月日搜索图片 | /year/month/day【url_param】 |
| /download | GET    | 下载指定图片             | /image_uuid【url_param】     |

- python调用

```python
import requests
import os

base_url="http://127.0.0.1:5555/"

# 上传一个图片
def upload():
    f=open(os.getcwd()+os.sep+"64304942_p0_master1200.jpg",mode="rb")
    file={"image":f}
    response=requests.post(base_url+"upload",files=file)
    print(response.json())

# 获取目录索引
def index():
    response=requests.get(base_url).json()
    print(response)

# 获取所有图片信息
def get_all():
    response=requests.get(base_url+"all").json()
    print(response)
```

#### 问题反馈

​	任何问题欢迎在[Issues](https://github.com/srx-2000/beierImage/issues) 中反馈。

　你的反馈会让此项目变得更加完美。

#### 贡献代码

​	本项目主要用于想要自己搭建私人图床使用，功能还并未完善，如果发现bug或有新的功能添加，请在[Issues](https://github.com/srx-2000/beierImage/issues) 中提交bug(或新功能)描述，我会尽力改进，使她更加完美。同时也希望大家可以通过star与fork来支持本项目。

#### 特别感谢

​	在此特别鸣谢[proxy_pool](https://github.com/jhao104/proxy_pool)项目，本项目关于flask部分的应用以及README等文档的编写，很多地方都参考了该项目。其本身是一个非常优秀的代理池技术。

