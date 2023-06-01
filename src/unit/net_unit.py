import aiohttp

from src.unit.file_unit import FileUnit


class NetUnit:
    @staticmethod
    async def get_request(url: str, dataPath: str, params = None):
        bangumiSetting = FileUnit.readBangumiSettingFile(dataPath)
        headers = {
            "User-Agent"   : f"banned/Anime-Qbittorrent/{bangumiSetting['version']} (https://github.com/banned2054/Anime-Qbittorrent)",
            "Authorization": f"Bearer {bangumiSetting['bangumi_token']}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers = headers, params = params) as response:
                if response.status == 200:
                    try:
                        responseData = await response.json()
                        return responseData
                    except aiohttp.ClientResponseError:
                        return "Error: Failed to parse JSON"
                else:
                    return f"Error: {response.status}"
