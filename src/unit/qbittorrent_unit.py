import asyncio

import qbittorrentapi

from src.unit.file_unit import FileUnit


class QbittorrentUnit:
    @staticmethod
    async def downloadOneFile(dataPath: str,
                              torrentPath: str,
                              fileName: str,
                              tag: str):
        qbittorrentSetting = FileUnit.readQbittorrentSettingFile(dataPath)
        conn_info = dict(
                host = qbittorrentSetting['host'],
                port = qbittorrentSetting['port'],
                username = qbittorrentSetting['userName'],
                password = qbittorrentSetting['password'],
        )
        qb = qbittorrentapi.Client(**conn_info)
        startTorrentList = {torrent.hash: torrent for torrent in qb.torrents_info()}
        with open(torrentPath, 'rb') as f:
            torrent_content = f.read()
        qb.torrents_add(torrent_files = torrent_content,
                        savepath = qbittorrentSetting['downloadPath'],
                        is_paused = True)
        await asyncio.sleep(2)
        endTorrentList = {torrent.hash: torrent for torrent in qb.torrents_info()}
        newTorrents = set(endTorrentList) - set(startTorrentList)
        newTorrentHash = newTorrents.pop()
        qb.torrents_rename(torrent_hash = newTorrentHash, new_torrent_name = fileName.split('/')[-1])
        qb.torrents_rename_file(torrent_hash = newTorrentHash, file_id = 0, new_file_name = fileName)
        qb.torrents_add_tags(torrent_hashes = newTorrentHash, tags = tag)
        qb.torrents_recheck(newTorrentHash)
        await asyncio.sleep(10)
        qb.torrents_resume(newTorrentHash)
        qb.torrents_reannounce(torrent_hashes = newTorrentHash)
