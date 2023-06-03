from src.unit.net_unit import NetUnit


class BangumiUnit:
    @staticmethod
    async def getAnimeInfoByBangumiId(dataPath: str, bangumiId: int):
        subject_url = f"https://api.bgm.tv/v0/subjects/{bangumiId}"
        responseData = await NetUnit.getBangumiRequest(dataPath, subject_url)
        if isinstance(responseData, str):
            return responseData
        result = {"date"   : responseData.get("date"), "name": responseData.get("name"),
                  "name_cn": responseData.get("name_cn"), "subject_id": bangumiId}
        return result

    @staticmethod
    async def searchAnimeByKeyword(dataPath: str, keyword: str):
        keyword = keyword.replace(' ', '%20')
        params = {'type': 2}
        url = f"https://api.bgm.tv/search/subject/{keyword}"
        responseData = await NetUnit.getBangumiRequest(dataPath, url, params)
        if isinstance(responseData, str):
            return responseData
        result = []
        for item in responseData['list']:
            bangumiId = int(item["url"].split("/")[-1])
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

    @staticmethod
    async def getAnimeEpisodeInfoByBangumiId(dataPath: str, bangumiId: int):
        url = f"https://api.bgm.tv/v0/episodes"
        params = {"subject_id": bangumiId}
        items = await NetUnit.getBangumiRequest(dataPath, url, params)
        if isinstance(items, str):
            return
        episodes = []
        for item in items['data']:
            if item['ep'] != 0:
                episodes.append(item['sort'])
        return episodes

# test
# asyncio.run(BangumiUnit.getAnimeEpisodeInfoByBangumiId('../data', 325585))
