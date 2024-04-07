import json
import requestsToAnilist
import time
from collections import OrderedDict
import qbittorrentapi
import os


def mainLoop(userid, feeds, rootSavePath, sleepTime, qbt_client):
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    while True:
        oldTitlesList = list(qbt_client.rss_rules().keys())
        watchlist = requestsToAnilist.getUserWatchList(userid, 0)
        if not watchlist:
            print("empty watchlist or error on anilistAPI sleeping for 1 minutes")
            time.sleep(60)
            continue
        for anime in watchlist:
            romajiTitle = anime["media"]["title"]["romaji"]
            if romajiTitle in oldTitlesList:
                oldTitlesList.remove(romajiTitle)
                continue

            englishTitle = anime["media"]["title"]["english"]
            synonyms = anime["media"]["synonyms"]
            possibleTitles = [romajiTitle, englishTitle] + synonyms
            regex = getRegex(possibleTitles)
            savePath = rootSavePath + romajiTitle

            ruleTemp = makeRuleTemplate(savePath=savePath, regex=regex, feeds=feeds)
            qbt_client.rss_set_rule(rule_name=romajiTitle, rule_def=ruleTemp)

        for romajiTitle in oldTitlesList:
            qbt_client.rss_removeRule(rule_name=romajiTitle)

        print("startSleeping for: " + str(sleepTime/60) + " hours and " + str(sleepTime%60) + " minutes")
        time.sleep(sleepTime*60)
        """end of cycle"""


def main():
    if "config.json" not in os.listdir(os.getcwd()):
        configUserid = int(os.environ.get("anilistuserid"))
        configClientid = os.environ.get("client_id")
        configClientsecret = os.environ.get("client_secret")
        configTorrentHost = os.environ.get("torrentHost")
        configTorrentPort = os.environ.get("torrentPort")
        configTorrentUsername = os.environ.get("torrentUsername")
        configTorrentPassword = os.environ.get("torrentPassword")
        configFeeds = os.environ.get("feeds")
        configRootSavePath = os.environ.get("rootSavePath")
        configSleepTime = int(os.environ.get("sleepTime"))
    else:
        with open("config.json", "r") as file:
            config = json.load(file)
        configUserid = config["anilistuserid"]
        configClientid = config["client_id"]
        configClientsecret = config["client_secret"]
        configTorrentHost = config["torrentAPI"]["host"]
        configTorrentPort = config["torrentAPI"]["port"]
        configTorrentUsername = config["torrentAPI"]["username"]
        configTorrentPassword = config["torrentAPI"]["password"]
        configFeeds = config["feeds"]
        configRootSavePath = config["rootSavePath"]
        configSleepTime = config["sleepTime"]

    if configUserid == -1:
        requestsToAnilist.doSetup(configClientid, configClientsecret)
    conn_info = dict(
        host=configTorrentHost,
        port=configTorrentPort,
        username=configTorrentUsername,
        password=configTorrentPassword,
    )
    qbt_client = qbittorrentapi.Client(**conn_info)
    mainLoop(userid=configUserid, feeds=configFeeds, rootSavePath=configRootSavePath,
             sleepTime=configSleepTime, qbt_client=qbt_client)


def makeRuleTemplate(savePath, regex, feeds):
    ruleAPI = {}
    ruleAPI["useRegex"] = True
    ruleAPI["smartFilter"] = True

    ruleAPI["mustContain"] = regex
    ruleAPI["affectedFeeds"] = feeds
    ruleAPI["savePath"] = savePath

    return ruleAPI

def getRegex(titles):
    titles = list(OrderedDict.fromkeys(titles))
    fotherWords = ["season", "part", "act", "final", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]
    romanNumeration = ["V", "I"]
    # "(TV)"
    # remove digit  "02"
    # remove fother "final"
    # remove romanNumeration "II"
    for j in range(5): #arbitrary number just to be sure all the junk gets removed
        for i in range(len(titles)):
            titleWords = titles[i].split()
            if titleWords[-1][-1] == ")" and titleWords[-1][0] == "(":
                titleWords.remove(titleWords[-1])
            elif titleWords[-1].isdigit():
                titleWords.remove(titleWords[-1])
            elif titleWords[-1].lower() in fotherWords:
                titleWords.remove(titleWords[-1])
            elif titleWords[-1][0] in romanNumeration and titleWords[-1][-1] in romanNumeration:
                titleWords.remove(titleWords[-1])

            titles[i] = ' '.join(titleWords) # titleWords is the words of one title so we are adding one title per iteration

    moreTitles = []
    for i in range(len(titles)):
        if ":" in titles[i]:
            aux = titles[i].split(":")[0]
            if aux.lower() != "re":
                moreTitles += [aux]
            moreTitles += [aux + " " + titles[i].split(":")[1]]
    titles += moreTitles

    titles = list(OrderedDict.fromkeys(titles))

    regex = str(titles[0])
    for i in range(1, len(titles)):
        regex += "|" + str(titles[i])
    return regex


if __name__ == "__main__":
    main()

