import pymysql.cursors

connection = pymysql.connect(
    host="localhost",
    user = "user",
    password="password",
    database="db",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)