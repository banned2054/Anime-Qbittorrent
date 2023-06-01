import sqlite3


class SqlUnit:
    @staticmethod
    def getAllData(dataPath: str):
        connection = sqlite3.connect(f'{dataPath}/anime.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM anime')
        rows = cursor.fetchall()
        connection.close()
        return rows

    @staticmethod
    def getDataByBangumiId(dataPath: str, bangumi_id: int):
        connection = sqlite3.connect(f'{dataPath}/anime.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM anime where bangumi_id = {bangumi_id}')
        rows = cursor.fetchall()
        connection.close()
        return rows

    @staticmethod
    def insertSqlNewLine(dataPath: str, bangumi_id: int, anime_name: str,
                         anime_cn_name: str, year: int, month: int, day: int):
        connection = sqlite3.connect(f'{dataPath}/anime.db')
        cursor = connection.cursor()
        cursor.execute(
                'INSERT INTO anime (name,name_cn,bangumi_id,publish_year,public_month,public_day) VALUES (?, ?, ?, ?, ?, ?)',
                (anime_name, anime_cn_name, bangumi_id, year, month, day))
        # 提交事务
        connection.commit()
        # 关闭到数据库的连接
        connection.close()
