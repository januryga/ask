from xgoogle.search import GoogleSearch, SearchError



raw_input=raw_input("What do you want to search?: ")
try:
  gs = GoogleSearch(str(raw_input))
  gs.results_per_page = 50
  results = gs.get_results()
  for res in results:
    print res.title.encode("utf8")
    print res.desc.encode("utf8")
    print res.url.encode("utf8")
    print
except SearchError, e:
  print "Search failed: %s" % e