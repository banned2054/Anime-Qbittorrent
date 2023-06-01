import os
import shutil

import yaml


class FileUnit:

    @staticmethod
    def initQbittorrentSetting(dataPath):
        if os.path.exists(f'{dataPath}/qbittorrent.yaml'):
            return
        shutil.copy(f'{dataPath}/qbittorrent.yaml.bak', f'{dataPath}/qbittorrent.yaml')

    @staticmethod
    def readQbittorrentSettingFile(dataPath):
        with open(f'{dataPath}/qbittorrent.yaml', 'r') as file:
            qbittorrentSettingData = yaml.safe_load(file)
            return qbittorrentSettingData

    @staticmethod
    def readBangumiSettingFile(dataPath):
        with open(f'{dataPath}/bangumi.yaml', 'r') as file:
            bangumiSettingData = yaml.safe_load(file)
            return bangumiSettingData

    @staticmethod
    def freshQbittorrentSettingFile(newQbittorrentSetting, dataPath):
        with open(f'{dataPath}/qbittorrent.yaml', 'w') as file:
            yaml.safe_dump(newQbittorrentSetting, file)
