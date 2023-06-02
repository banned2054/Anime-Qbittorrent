import asyncio

import qbittorrentapi

from src.unit.file_unit import FileUnit


class QbittorrentUnit:
    @staticmethod
    async def downloadOneFile(dataPath: str,
                              torrent_path: str,
                              file_name: str,
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
        with open(torrent_path, 'rb') as f:
            torrent_content = f.read()
        qb.torrents_add(torrent_files = torrent_content,
                        savepath = qbittorrentSetting['downloadPath'],
                        is_paused = True)
        await asyncio.sleep(2)
        endTorrentList = {torrent.hash: torrent for torrent in qb.torrents_info()}
        new_torrents = set(endTorrentList) - set(startTorrentList)
        new_torrent_hash = new_torrents.pop()
        qb.torrents_rename(torrent_hash = new_torrent_hash, new_torrent_name = file_name.split('/')[-1])
        qb.torrents_rename_file(torrent_hash = new_torrent_hash, file_id = 0, new_file_name = file_name)
        qb.torrents_add_tags(torrent_hashes = new_torrent_hash, tags = tag)
        qb.torrents_recheck(new_torrent_hash)
        await asyncio.sleep(10)
        qb.torrents_resume(new_torrent_hash)
        qb.torrents_reannounce(torrent_hashes = new_torrent_hash)
