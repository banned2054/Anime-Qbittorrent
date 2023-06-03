import asyncio
import json
from xml.etree import ElementTree

import aiohttp

from src.unit.file_unit import FileUnit


class NetUnit:
    @staticmethod
    async def getBangumiRequest(dataPath: str, url: str, params = None):
        bangumiSetting = FileUnit.readBangumiSettingFile(dataPath)
        headers = {
            "User-Agent"   : f"banned/Anime-Qbittorrent/{bangumiSetting['version']} (https://github.com/banned2054/Anime-Qbittorrent)",
            "Authorization": f"Bearer {bangumiSetting['bangumiToken']}"
        }
        originResult = await NetUnit.getResponseData(url, headers, params)
        if originResult.startswith('Error:'):
            return originResult
        try:
            jsonResult = json.loads(originResult)
            return jsonResult
        except json.JSONDecodeError:
            return "Error: Failed to parse JSON"
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    async def getMikanRequest(url: str, proxy = None):
        originResult = await NetUnit.getResponseData(url, proxy = proxy)
        try:
            elementResult = ElementTree.fromstring(originResult)
            NetUnit.printTree(elementResult)
            return elementResult
        except ElementTree.ParseError:
            return "Error: Failed to parse XML"
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    async def getResponseData(url: str, headers = None, params = None, proxy = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers = headers, params = params, proxy = proxy) as response:
                if response.status == 200:
                    result = await response.text()
                    return result
                else:
                    return f"Error: {response.status}"

    @staticmethod
    def printTree(element, indent = 0):
        print(' ' * indent + element.tag)
        for child in element:
            NetUnit.printTree(child, indent + 2)


asyncio.run(NetUnit.getMikanRequest(
        'https://mikanani.me/RSS/MyBangumi?token=ZoVG3vGFwo5h1JXB8A0FiA%3d%3d',
        proxy = 'http://127.0.0.1:7890'))
