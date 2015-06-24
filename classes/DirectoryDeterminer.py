"""
DirectoryDeterminer.py
"""


class DirectoryDeterminer:
	
	
	
	def determineEnclosingDirectory(self, path):
		# assumes path doesn't end with a "/", i.e., determined by os.path.abspath('')
		lastSlashPosition = path.rfind("/")
		buffer = path[0:lastSlashPosition]
		enclosingDirectory = buffer + "/" # I want the slash for a sys.path.append	
		return enclosingDirectory
	
	
	
	def determineRunningScript(self, path):
		lastSlashPosition = path.rfind("/")
		startPosition = lastSlashPosition + 1
		scriptName = path[startPosition:]
		return scriptName



# bottom