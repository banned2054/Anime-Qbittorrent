import sqlite3


class SqlUnit:
    @staticmethod
    def initSql(dataPath: str):
        connection = sqlite3.connect(f'{dataPath}/anime.db')
        cursor = connection.cursor()
        cursor.execute("""create table anime(
                        name         varchar(50) not null,
                        name_cn      varchar(50),
                        publish_year int,
                        public_month int,
                        public_day   int,
                        bangumi_id   varchar(20) primary key
        );
        """)
        # 提交事务
        connection.commit()
        # 关闭到数据库的连接
        connection.close()

    @staticmethod
    def getAllData(dataPath: str):
        connection = sqlite3.connect(f'{dataPath}/anime.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM anime ORDER BY publish_year DESC, public_month DESC, public_day, name')
        rows = cursor.fetchall()
        connection.close()
        return rows

    @staticmethod
    def getDataByBangumiId(dataPath: str, bangumi_id: int):
        connection = sqlite3.connect(f'{dataPath}/anime.db')
        cursor = connection.cursor()
        cursor.execute(
                f'SELECT * FROM anime where bangumi_id = {bangumi_id} ORDER BY publish_year DESC, public_month DESC, public_day, name')
        rows = cursor.fetchall()
        connection.close()
        return rows

    @staticmethod
    def getDataByAnimeName(dataPath: str, animeName: str):
        connection = sqlite3.connect(f'{dataPath}/anime.db')
        cursor = connection.cursor()
        animeName = f'\"{animeName}\"'
        cursor.execute(
                f'SELECT * FROM anime where name = {animeName} ORDER BY publish_year DESC, public_month DESC, public_day, name')
        rows = cursor.fetchall()
        connection.close()
        return rows

    @staticmethod
    def insertSqlNewLine(dataPath: str, bangumiId: int, animeName: str,
                         animeCnName: str, year: int, month: int, day: int):
        connection = sqlite3.connect(f'{dataPath}/anime.db')
        cursor = connection.cursor()
        cursor.execute(
                'INSERT INTO anime (name,name_cn,bangumi_id,publish_year,public_month,public_day) VALUES (?, ?, ?, ?, ?, ?)',
                (animeName, animeCnName, bangumiId, year, month, day))
        # 提交事务
        connection.commit()
        # 关闭到数据库的连接
        connection.close()
