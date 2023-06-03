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
        items = element.findall(".//item")
        for item in items:
            enclosure = item.find('enclosure')
            if enclosure is not None:  # 确保 'enclosure' 元素存在
                enclosure_url = enclosure.get('url')  # 获取 'url' 属性
            # 获取 'torrent' 元素的 'pubDate' 子元素
            torrent = item.find('{https://mikanani.me/0.1/}torrent')
            if torrent is not None:  # 确保 'torrent' 元素存在
                pub_date = torrent.find('{https://mikanani.me/0.1/}pubDate')
                if pub_date is not None:  # 确保 'pubDate' 元素存在
                    pub_date_text = pub_date.text  # 获取 'pubDate' 的文本内容
            print(item.find('title').text)
            print(item.find('link').text)
            print(enclosure_url)
            print(pub_date_text)
            print('---')

    @staticmethod
    def downloadFile(url: str, fileName: str, proxy = None):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy = proxy) as resp:
                    if resp.status != 200:
                        print(f"Error: Failed to download file")
                        return False
                    with open(fileName, 'wb') as file:
                        while True:
                            chunk = await resp.content.read(1024)  # 读取文件内容
                            if not chunk:
                                break
                            file.write(chunk)  # 写入文件
            return True
        except Exception as e:
            print(f"Error: Failed to download file")
            return False


asyncio.run(NetUnit.getMikanRequest(
        'https://mikanani.me/RSS/MyBangumi?token=ZoVG3vGFwo5h1JXB8A0FiA%3d%3d',
        proxy = 'http://127.0.0.1:7890'))
