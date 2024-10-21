# 查询数学成绩大于90分的学生
import sqlite3

conn = sqlite3.connect('local_rag.db')
# 创建一个表
cur = conn.cursor()x