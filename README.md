# RuleMaker-Anilist

This tool is used to automate rules for qbit of animes from your Anilist Watchlist.

### Setup

- Make sure you have all the dependencies installed.
- Edit `config.json` file to configure the tool.

### Usage
- `1st step`: go to anilist under settings->apps->developer->create new client. Then just put something random on the app name and leave the redirect url empty
- `2nd step`: copy the ID to `config.json`->`client_id` and the Secret to `config.json`->`client_secret`
- `3rd step`: fill the rest of `config.json` as it is explained on parametres (note you will mostlikely not know ur `userid` until the first execution of the tool)
- `4th step`: run & fill userid with the id you got the tool will print ("Your user id is: " if sucefull)
- `5th step`: run and enjoy

### Input Parameters

- `userid`: userid
  - Anilist userid (run the program the 1st time with at least `client_id` and `client_secret` filled)
- `client_id` & `client_secret`: client id & client secret
  - Explained how to get in `Usage`
- `sleepTime`: sleep time
  - time betteween requests to anilist in minutes, by default is set to 24h, restarting the program will force a update(if u dont wanna wait)
- `feeds`: ["feed1", "feed2"]
  - List of feeds to scrape.
- `rootSavePath`: your media folder path
  - The parent folder where all other anime folders will be added. Other folders will have the Romanji Title.
- `torrent`:
  - `host`: your torrent client host
  - `port`: your torrent client port
  - `username`: your torrent client username
  - `password`: your torrent client password

### Output

There is no visible output this will add the rules directly to our qbit WEBUI

### Disclaimer

Be responsible, with this and follow ur country piracy/copyright laws.
