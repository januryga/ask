from search import GoogleSearch, SearchError



#raw_input=raw_input("What do you want to search?: ")
def get_google_search(phrase):
  try:
    gs = GoogleSearch(phrase)
    gs.results_per_page = 50
    results = gs.get_results()
    if not results:
      print "No results matched."
    else:
      for res in results:
        print res.title.encode("utf8")
        print res.desc.encode("utf8")
        #print res.url.encode("utf8")
        print
  except SearchError:
    print "Google search failed"
#get_google_search(str(raw_input))
