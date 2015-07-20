# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class DirectoryDeterminer( object ):

	def determineEnclosingDirectory(self, path):
		lastSlashPosition = path.rfind("/")  # assumes path doesn't end with a "/", i.e., determined by os.path.abspath('')
		buffer = path[0:lastSlashPosition]
		enclosingDirectory = buffer + "/" # I want the slash for a sys.path.append
		return enclosingDirectory

	def determineRunningScript(self, path):
		lastSlashPosition = path.rfind("/")
		startPosition = lastSlashPosition + 1
		scriptName = path[startPosition:]
		return scriptName

    # end class DirectoryDeterminer
