userID = '''
query{
    Viewer{
		id
	}
}
'''

userWatchList = '''
query ($userId: Int, $page: Int) {
  Page(page: $page) {
    pageInfo {
      hasNextPage
    }
    mediaList(userId: $userId, status: CURRENT, type: ANIME) {
      media {
        title {
            romaji
            english
        }
        synonyms
      }
    }
  }
}
'''