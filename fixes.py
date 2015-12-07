""" A containment zone for ugly hotfixes. """


# Doesn't work for some mysterious reason.
#
# def disable_unicode():
# 	"""Disables unicode characters in in program
# 	input and output, it seems. At least it prevents 
# 	Windows from crying about a UnicodeException every
# 	10 goddamn seconds.

# 	Source: http://goo.gl/6rh4vo
# 	( http://stackoverflow.com/a/3259271/5534735 )"""

# 	import codecs
# 	codecs.register(
# 		lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None
# 	)

def asciified(string):
	encoded = string.encode('ascii', 'replace')
	return encoded.decode('ascii')