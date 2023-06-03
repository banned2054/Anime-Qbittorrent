from src.unit.file_unit import FileUnit


class MikanUnit:
    @staticmethod
    def addOriginRss(dataPath: str, token: str):
        mikanSetting = FileUnit.readMikanSettingFile(dataPath)
        mikanSetting['token'] = token
        FileUnit.freshMikanSettingFile(dataPath, mikanSetting)
