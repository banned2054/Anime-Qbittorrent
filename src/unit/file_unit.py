import os
import shutil

import bencodepy
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
    def freshQbittorrentSettingFile(dataPath, newQbittorrentSetting):
        with open(f'{dataPath}/qbittorrent.yaml', 'w') as file:
            yaml.safe_dump(newQbittorrentSetting, file)

    @staticmethod
    def getTorrentOneFileName(torrentPath: str):
        fileName = ""
        with open(torrentPath, 'rb') as f:
            data = bencodepy.decode(f.read())
            if b'files' in data[b'info']:
                files = data[b'info'][b'files']
                for file in files:
                    if b'path.utf-8' in file:
                        fileName = '/'.join([x.decode() for x in file[b'path.utf-8']])
                    else:
                        fileName = file[b'path'].decode()
            else:
                fileName = data[b'info'][b'name'].decode()
        return fileName

    @staticmethod
    def deleteFile(filePath: str):
        os.remove(filePath)
