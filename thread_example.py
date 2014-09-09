#!/usr/bin/env python
#https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz
#https://download.mozilla.org/?product=firefox-32.0-SSL&os=linux64&lang=en-US

import threading
import time
import urllib2

FILES_TO_DOWNLOAD = [
	['https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz', 'python.tar.xz'],
	['https://download.mozilla.org/?product=firefox-32.0-SSL&os=linux64&lang=en-US', 'firefox.tar.bz2']
]

def download(event, url, filename):
	firefox = urllib2.urlopen(url)
	firefox_file = open('firefox.tar.bz2', 'wb')
	firefox_file.write(firefox.read())
	event.set()


def main():
	threads = []
	event = threading.Event()
	start_time = time.time()
	for files in FILES_TO_DOWNLOAD:
		thread = threading.Thread(target=download, args=(event, files[0], files[1]))
		threads.append(thread)
		thread.start()
	for thread in threads:
		thread.join()
	event.wait()
	elasped = time.time() - start_time
	print(elasped)
	return 0

if __name__ == '__main__':
	main()

