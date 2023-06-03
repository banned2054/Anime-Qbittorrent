import os.path

from src.unit.file_unit import FileUnit
from src.unit.net_unit import NetUnit
from src.unit.string_unit import StringUnit


class MikanUnit:
    @staticmethod
    def addOriginRss(dataPath: str, token: str):
        mikanSetting = FileUnit.readMikanSettingFile(dataPath)
        mikanSetting['token'] = token
        FileUnit.freshMikanSettingFile(dataPath, mikanSetting)

    @staticmethod
    async def freshRss(dataPath: str):
        mikanSetting = FileUnit.readMikanSettingFile(dataPath)
        url = ''
        if mikanSetting['useReverseProxy']:
            url = mikanSetting['customUrl']
        else:
            if mikanSetting['token'] == 'None' or mikanSetting['token'] is None or mikanSetting['token'] == '':
                return
            url = f"{mikanSetting['customUrl']}/RSS/MyBangumi?token={mikanSetting['token']}"
        proxy = None
        if mikanSetting['proxy']['useProxy']:
            proxy = f"{mikanSetting['proxy']['proxyUrl']}:{mikanSetting['proxy']['port']}"
        xmlResult = await NetUnit.getMikanRequest(url, proxy)
        if isinstance(xmlResult, str):
            # todo
            pass
        lastDate = mikanSetting['finalPubDate']
        items = xmlResult.findall(".//item")
        for item in items:
            torrent = item.find('{https://mikanani.me/0.1/}torrent')
            if torrent is not None:  # 确保 'torrent' 元素存在
                pub_date = torrent.find('{https://mikanani.me/0.1/}pubDate')
                if pub_date is not None:  # 确保 'pubDate' 元素存在
                    pub_date_text = pub_date.text  # 获取 'pubDate' 的文本内容
                    if StringUnit.firstTimeLaterThanSecond(pub_date_text, lastDate):
                        enclosure = item.find('enclosure')
                        if enclosure is not None:  # 确保 'enclosure' 元素存在
                            torrentUrl = enclosure.get('url')  # 获取 'url' 属性
                            torrentFilePath = f"{dataPath}/cache/{os.path.basename(torrentUrl)}"
                            downloadResult = await NetUnit.downloadFile(torrentUrl, torrentFilePath, proxy)
