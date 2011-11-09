#!/usr/bin/env python

import os, sys, re

def main(home_dir):
	CONFIG_DIR='config'
	for config in os.listdir(CONFIG_DIR):
		src = os.path.abspath(os.sep.join([CONFIG_DIR, config]))
		dst = os.sep.join([home_dir, '.%s' % config])
		if os.path.islink(dst):
			if os.readlink(dst) == src:
				continue

			msg = 'Link %s already exists to %s'
			print msg % (dst, os.readlink(dst))
			if raw_input('Would you like replace it? (Y/n)') in ['y', '']:
				os.remove(dst)
			else:
				print 'ignoring file %s' % src
				continue

		if os.path.exists(dst):
			os.system('diff -u %s %s | less' % (dst, src))
			if raw_input('Substitute (Y/n) ').lower() in ['y', '']:
				os.rename(dst, dst + '.bk')
			else:
				print 'ignoring file %s' % src
				continue

		os.symlink(src, dst)
		print '$ ln -s %s %s' % (src, dst)
	print 'done.'

if __name__ == '__main__':
	if len(sys.argv) > 1:
		home_dir = sys.argv[1]
	else:
		home_dir = os.path.expanduser('~')
	home_dir = re.sub('/*$', '', home_dir)
	main(home_dir)
