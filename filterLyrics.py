#!/usr/bin/env python
from eyeD3 import Mp3AudioFile
import unicodedata
import urllib2
from BeautifulSoup import BeautifulSoup
import sys, re, os

BASE_URL = 'http://www.vagalume.com.br'
PAGE_EXT = '.html'

class Lyrics():
	def __init__(self, mp3_file):
		try:
			self.mp3 = Mp3AudioFile(mp3_file)
		except:
			print 'File: %s is not a mp3 file' % mp3_file
			sys.exit(1)

		self.tag = self.mp3.getTag()
		self.url = None
		self.lyric = None

	def makeURL(self):
		artist = self.__normalize__(self.tag.getArtist())
		title = self.__normalize__(self.tag.getTitle())
		url_artist = artist.replace(' ', '-').lower()
		url_title = title.replace(' ', '-').lower()
		url = '/'.join([
			BASE_URL,
			url_artist,
			url_title,
		])
		self.url = url + PAGE_EXT
		return self.url

	def makeFile(self, mp3_file=None):
		dir_lyrics = 'lyrics'
		if not os.path.isdir(dir_lyrics):
			os.makedirs(dir_lyrics)
		mp3_file = self.mp3.fileName if mp3_file is None else mp3_file
		out = re.search(r'.*\.', mp3_file)
		mp3_save = "%s/%slyric" % (dir_lyrics, out.group(0))
		return mp3_save

	def saveLyric2File(self, lyric=None, save_file=None):
		lyric = self.lyric if lyric is None else lyric
		save_file = self.makeFile() if save_file is None else save_file

		artist = self.__normalize__(self.tag.getArtist())
		title = self.__normalize__(self.tag.getTitle())
		lyric = "Artist: %s\nTitle: %s\n\n%s" % (artist, title, lyric)

		f = open(save_file, 'w')
		try:
			lyric = lyric.encode('utf8')
			f.write(lyric.replace('\r', ''))
		except:
			f.write(lyric.replace('\r', ''))
		f.close()

	def getLyricFromURL(self, url=None):
		url = self.url if url is None else url
		appends = ['', '-letras']
		for i, app in enumerate(appends):
			url_cur = url.replace('.html', '%s.html' % app)
			try:
				return self.__getLyricFromURL__(url_cur)
			except Exception as e:
				print 'trying error with url: %s' % url_cur
				if str(e) == 'html_tag is zero' and i+1 == len(appends):
					print 'Error to get html tag'


	def __getLyricFromURL__(self, url):
		if url is None:
			# Url not defined and not passed
			print 'No url found'
			raise Exception('No url found')

		url_opened = urllib2.urlopen(url)
		self.html = url_opened.read()
		self.lyric = self.__parseHTML__(self.html)
		return self.lyric

	def getLyricFromMP3(self, mp3=None):
		mp3 = self.mp3 if mp3 is None else mp3
		try:
			return self.__getLyricFromMP3__(mp3)
		except:
			return False

	def __getLyricFromMP3__(self, mp3):
		tag = mp3.getTag()
		lyric = list()
		for l in tag.getLyrics():
			lyric.append(l.lyrics)

		self.lyric = '\n'.join(lyric)
		return self.lyric

	def __normalize__(self, string):
		nkfd_form = unicodedata.normalize('NFKD', unicode(string))
		only_ascii = nkfd_form.encode('ASCII', 'ignore')
		return only_ascii

	def __parseHTML__(self, html, app=0):
		soup = BeautifulSoup(html)
		html_tag = soup.findAll('span', {'class':"editable_area"})

		if len(html_tag) == 0:
			raise Exception('html_tag is zero')

		html_lyric = html_tag[0].renderContents().replace('\n', '')
		br = r'\s*<\s*br\s*/?\s*>'
		lyric = re.sub(br, '\n', html_lyric)

		return lyric

def debug(mp3_file, lyric):
	mp3_html = '%s.debug' % mp3_file
	html = getattr(lyric, 'html', '')
	print 'Error to parse html, read %s' % mp3_html

	f = open(mp3_html, 'w')
	f.write("URL: %s\n" % lyric.url)
	f.write("HTML: \n")
	f.write(html)
	f.close()

if __name__ == '__main__':
	mp3_file = sys.argv[1].decode('utf8')
	a = Lyrics(mp3_file)
	lyric = a.getLyricFromMP3()
	if not lyric:
		try:
			a.makeURL()
			url=None
			if len(sys.argv) > 2:
				url=sys.argv[2]
			lyric = a.getLyricFromURL(url)
		except:
			debug(mp3_file, a)
	a.saveLyric2File()
