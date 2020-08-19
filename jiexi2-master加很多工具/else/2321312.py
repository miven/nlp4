import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    database='guns',
    charset='utf8'
)
# 获取一个光标
cursor = conn.cursor()

# 定义要执行的sql语句
sql = 'select * from sys_dict'

# 拼接并执行sql语句
t=cursor.execute(sql)

# 涉及写操作要注意提交
conn.commit()

# 关闭连接
cursor.close()
conn.close()