# coding = utf-8
# 存放数据库密码，账号，Flask key等机密信息
# 开发环境相关信息
# 不上传到git服务器

STATUS = 'secure导入成功'
DEBUG = True
RUN_PORT = 80
RUN_HOST = '0.0.0.0'

#数据库相关
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:py123@localhost:3306/fisher'