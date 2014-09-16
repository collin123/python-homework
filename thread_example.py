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
	threads = {}
	event = threading.Event()
	start_time = time.time()
	for files in FILES_TO_DOWNLOAD:
		file_url = files[0]
		file_name = files[1]
		thread = threading.Thread(target=download, args=(event, file_url, file_name))
		threads[file_name] = thread
		thread.start()

	while threads:
		#import pdb; pdb.set_trace()
		dead_threads = []
		for file_name, thread in threads.items():
			if not thread.is_alive():
				dead_threads.append(file_name)
		for file_name in dead_threads:
			print(file_name + ' finished downloading')
			del threads[file_name]
	event.wait()
	elasped = time.time() - start_time
	print(elasped)
	return 0

if __name__ == '__main__':
	main()

