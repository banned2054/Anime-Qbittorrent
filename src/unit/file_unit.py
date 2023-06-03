import os
import shutil

import bencodepy
import yaml


class FileUnit:

    @staticmethod
    def initQbittorrentSetting(dataPath: str):
        if os.path.exists(f'{dataPath}/config/qbittorrent.yaml'):
            return
        shutil.copy(f'{dataPath}/config-back/qbittorrent.yaml.bak', f'{dataPath}/qbittorrent.yaml')

    @staticmethod
    def readQbittorrentSettingFile(dataPath: str):
        with open(f'{dataPath}/config/qbittorrent.yaml', 'r') as file:
            qbittorrentSettingData = yaml.safe_load(file)
            return qbittorrentSettingData

    @staticmethod
    def readBangumiSettingFile(dataPath: str):
        with open(f'{dataPath}/config/bangumi.yaml', 'r') as file:
            bangumiSettingData = yaml.safe_load(file)
            return bangumiSettingData

    @staticmethod
    def freshQbittorrentSettingFile(dataPath: str, newQbittorrentSetting):
        with open(f'{dataPath}/config/qbittorrent.yaml', 'w') as file:
            yaml.safe_dump(newQbittorrentSetting, file)

    @staticmethod
    def getTorrentOneFileName(torrentPath: str):
        fileName = ""
        with open(torrentPath, 'rb') as f:
            data = bencodepy.decode(f.read())
            # if b'files' in data[b'info']:
            #     files = data[b'info'][b'files']
            #     for file in files:
            #         path = ""
            #         for item in file[b'path']:
            #             path = f"{path}/{item.decode('utf-8')}"
            #         if path.__contains__('TC') or path.__contains__('tc'):
            #             continue
            #         if path.__contains__('mp4') or path.__contains__('mkv') or path.__contains__('ass'):
            #             pattern = re.compile(r'\[\d+\]')
            #             if pattern.search(path) or path.__contains__('OVA') or path.__contains__('ova'):
            #                 fileName = path
            # else:
            fileName = data[b'info'][b'name'].decode()
        return fileName

    @staticmethod
    def deleteFile(filePath: str):
        os.remove(filePath)

    @staticmethod
    def readMikanSettingFile(dataPath: str):
        with open(f'{dataPath}/config/mikan.yaml', 'r') as file:
            mikanSettingData = yaml.safe_load(file)
            return mikanSettingData

    @staticmethod
    def freshMikanSettingFile(dataPath: str, newMikanSetting):
        with open(f'{dataPath}/config/mikan.yaml', 'w') as file:
            yaml.safe_dump(newMikanSetting, file)

    @staticmethod
    def initMikanSetting(dataPath: str):
        if os.path.exists(f'{dataPath}/config/mikan.yaml'):
            return
        shutil.copy(f'{dataPath}/config-back/mikan.yaml.bak', f'{dataPath}/mikan.yaml')
