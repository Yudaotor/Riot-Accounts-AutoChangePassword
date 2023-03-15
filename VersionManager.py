import requests as req


class VersionManager:

    @staticmethod
    def getLatestTag():
        try:
            latestTagResponse = req.get("https://api.github.com/repos/Yudaotor/Riot-Accounts-AutoChangePassword/releases/latest")
            if 'application/json' in latestTagResponse.headers.get('Content-Type', ''):
                latestTagJson = latestTagResponse.json()
                if "tag_name" in latestTagJson:
                    return float(latestTagJson["tag_name"][1:])
            return 0.0
        except Exception as ex:
            print(ex)
            return 0.0

    @staticmethod
    def isLatestVersion(currentVersion):
        return currentVersion >= VersionManager.getLatestTag()

