#!/usr/bin/env python

import os, sys, re

def main(home_dir):
	CONFIG_DIR='config'
	for config in os.listdir(CONFIG_DIR):
		src = os.path.abspath(os.sep.join([CONFIG_DIR, config]))
		dst = os.sep.join([home_dir, '.%s' % config])
		if os.path.exists(dst):
			print 'file %s exists' % dst
			continue

		os.symlink(src, dst)
		print '$ ln -s %s %s' % (src, dst)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		home_dir = sys.argv[1]
	else:
		home_dir = os.path.expanduser('~')
	home_dir = re.sub('/*$', '', home_dir)
	main(home_dir)
