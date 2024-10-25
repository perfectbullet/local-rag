import sqlite3

from deal_excel_and_json import read_excel

if __name__ == '__main__':
    # 读取数据
    headers, recovered_json = read_excel('./医疗器械-产品详细1024整理.xlsx')
    # 导入SQLite驱动:

    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('local_rag.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    # 执行一条SQL语句，创建user表:
    # image_name	keywords	image_path
    # cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
    for data in recovered_json:
        cursor.execute(
            "INSERT OR REPLACE INTO keywords_to_image (image_name, keywords, image_path) VALUES (?, ?, ?)",
            (data['image_name'], data['keywords'], data['image_path'])
        )
    conn.commit()
    # 继续执行一条SQL语句，插入一条记录:
    cursor.execute('select * from keywords_to_image')

    # 通过rowcount获得插入的行数:
    print(cursor.rowcount)

    # 关闭Cursor:
    cursor.close()
    # 关闭Connection:
    conn.close()
