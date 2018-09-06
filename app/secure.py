# coding = utf-8

STATUS = 'secure导入成功'
DEBUG = True
RUN_PORT = 80
RUN_HOST = '0.0.0.0'
SECRET_KEY = 'RbfokkRe1gsZITyX!Ezxb#Bj&1yxNb1Z'

# 数据库相关
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/fisher'

# flask-mail Email 配置
# 邮箱服务器 端口号 等
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '1114524476@qq.com'
MAIL_PASSWORD = 'gmfauzarpzttgccg'
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SENDER = '1114524476@qq.com'

# 赠送成功奖励鱼豆数量
BEANS_EVERY_DRIFT = 2
BEANS_UPLOAD_ONE_BOOK = 1
