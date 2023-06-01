from src.unit.net_unit import NetUnit


class BangumiUnit:
    @staticmethod
    async def getAnimeInfoByBangumiId(dataPath: str, bangumiId: int):
        subject_url = f"https://api.bgm.tv/v0/subjects/{bangumiId}"
        responseData = await NetUnit.get_request(dataPath, subject_url)
        if isinstance(responseData, str):
            return responseData
        result = {"date"   : responseData.get("date"), "name": responseData.get("name"),
                  "name_cn": responseData.get("name_cn"), "subject_id": bangumiId}
        return result

    @staticmethod
    async def searchAnimeByKeyword(dataPath: str, keyword: str):
        params = {'type': 2}
        url = f"https://api.bgm.tv/search/subject/{keyword}"
        responseData = await NetUnit.get_request(url, dataPath, params)
        if isinstance(responseData, str):
            return responseData
        result = []
        for item in responseData:
            bangumiId = int(item.get("url").split("/")[-1])
            result.append(bangumiId)
        return result

    @staticmethod
    async def getAnimeInfoByMultiBangumiId(dataPath: str, bangumiIdList):
        result = []
        for bangumiId in bangumiIdList:
            item = await BangumiUnit.getAnimeInfoByBangumiId(dataPath, bangumiId)
            if isinstance(item, str):
                continue
            result.append(item)
        return result
