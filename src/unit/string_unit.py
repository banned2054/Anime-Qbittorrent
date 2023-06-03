from datetime import datetime


class StringUnit:
    @staticmethod
    def firstTimeLaterThanSecond(firstTime: str, sceondTime: str):
        # 解析日期字符串
        date1 = datetime.strptime(firstTime, "%Y-%m-%dT%H:%M:%S")
        date2 = datetime.strptime(sceondTime, "%Y-%m-%dT%H:%M:%S")

        # 比较日期并返回较晚的那个
        if date1 > date2:
            return True
        return False
