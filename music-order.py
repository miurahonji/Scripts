#!/usr/bin/env python

from eyeD3 import Mp3AudioFile
import unicodedata
import urllib2
from BeautifulSoup import BeautifulSoup
import sys, re, os

BASE_URL = 'http://www.vagalume.com.br'
PAGE_EXT = '.html'

class FileMusic():
	def __init__(self, mp3_file):
		self.mp3 = Mp3AudioFile(mp3_file)
		self.mp3_file = mp3_file
		self.tag = self.mp3.getTag()
		self.info = dict()

	def getInfo(self):
		self.info['title'] = self.__normalize__(self.tag.getTitle())
		self.info['track'] = int(self.tag.getTrackNum()[0])
		self.info['artist'] = self.__normalize__(self.tag.getArtist())
		self.info['album'] = self.__normalize__(self.tag.getAlbum())
		self.info['sep'] = os.sep
		self.__addNewInfo__('title', self.info)
		self.__addNewInfo__('track', self.info)
		self.__addNewInfo__('artist', self.info)
		self.__addNewInfo__('album', self.info)
		self.info['artist'] = re.sub(r'Feat.*', '', self.info['artist']).strip()

	def getNewName(self):
		return '%(track)02d - %(title)s.mp3' % self.info

	def getNewDir(self):
		return '%(artist)s%(sep)s%(album)s' % self.info

	def __addNewInfo__(self, key, info):
		if not info[key]:
			print 'file: %s' % self.mp3_file
			info[key] = raw_input('%s: ' % key)
			print
			if key == 'track':
				return

			getattr(self.tag, 'set%s' % key.capitalize())(info[key])

	def __normalize__(self, string):
		nkfd_form = unicodedata.normalize('NFKD', unicode(string))
		only_ascii = nkfd_form.encode('ASCII', 'ignore')
		return only_ascii

def __sort__(x, y):
	if x.endswith('.mp3') and not y.endswith('.mp3'):
		return -1
	if y.endswith('.mp3') and not x.endswith('.mp3'):
		return 1

	return 0

if __name__ == '__main__':
	albuns = dict()
	arg_1 = sys.argv[1].decode('utf8')
	arg_2 = sys.argv[2].decode('utf8')
	old_directory = re.sub(r'/*$', '', arg_1)
	new_directory = re.sub(r'/*$', '', arg_2)

	for root,dirs,files in os.walk(old_directory):
		files.sort(__sort__, reverse=True)
		for _file in files:
			mp3_file = os.sep.join([root, _file])
			try:
				a = FileMusic(mp3_file)
				a.getInfo()
				album = a.info['album']
				if not albuns.has_key(album):
					albuns[album] = [set(), list()]
				albuns[album][0] = albuns[album][0].union([a.info['artist']])
				albuns[album][1].append(a)
			except:
				continue
				name = os.path.basename(mp3_file)
				if not os.path.isdir(new_dir):
					os.makedirs(new_dir)
				new_name = os.sep.join([new_dir, 'info', name])
				print 'Renaming: "%s" -> "%s"' % (mp3_file, new_name)
				os.rename(mp3_file, new_name)

	for album in albuns.keys():
		artists, files = albuns[album]
		for a in files:
			if len(artists) > 1:
				print artists
				a.info['artist'] = 'Varios'

			new_name = a.getNewName()
			new_dir = os.sep.join([new_directory, a.getNewDir()])
			if not os.path.isdir(new_dir):
				os.makedirs(new_dir)
			new_name = os.sep.join([new_dir, new_name])
			os.rename(a.mp3_file, new_name)
