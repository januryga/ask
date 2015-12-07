""" Search Google, duh."""

from search import GoogleSearch, SearchError


def search_results(phrase):
	try:
		gs = GoogleSearch(phrase)
		gs.results_per_page = 30
		results = gs.get_results()
		if not results:
			result = "No results matched."
		else:
			str_list=[]
			for res in results:
				str_list.append(res.title.encode("utf8"))
				str_list.append(res.desc.encode("utf8"))
			return '\n'.join(str_list)
	except SearchError:
		result = "Google search failed."
	return result
