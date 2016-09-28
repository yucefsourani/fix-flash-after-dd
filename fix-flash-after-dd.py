#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  fix-flash-after-dd.py
#  
#  Copyright 2016 youcefsourani <youssef.m.sourani@gmail.com>
#  
#  www.arfedora.blogspot.com
#
#  www.arfedora.com
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
#  
#  
import os
import subprocess
import sys

def init_check():
	if os.getuid()!=0:
		exit("Run Script With Root Permissions.")
		
	if not sys.version.startswith("3"):
		sys.exit("Use Python 3 Try run python3 fix-flash-after-dd.py")
init_check()


def is_correct_directory(directory):
	if os.path.exists(directory):
		if directory[-1].isalpha() and directory[5:-1]=="sd" and directory[-1]!="a":
			return True
		else:
			return False
	else:
		return False
		

def welcome(error=""):
	while True:
		subprocess.call("clear")
		print("http://arfedora.blogspot.com")
		if len(error)!=0:
			print("\n%s"%error)
		print ("\nType q To Quit.")
		print ("\nEnter USB Flash Memory Directory Ex: /dev/sdb :")
		answer=input("-").strip()
		if answer=="q" or answer=="Q":
			sys.exit("\nBye...\n")
		elif is_correct_directory(answer):
			while True:
				subprocess.call("clear")
				print("http://arfedora.blogspot.com")
				print ("\nType q To Quit.")
				print ("\nWARNING! ALL DATA ON DRIVE %s WILL BE LOST!"%answer)
				print ("\nN To Back || Y To Contiune || Q To Quit.")
				answer1=input("-").strip()
				if answer1=="q" or answer1=="Q":
					sys.exit("\nBye...\n")
				elif answer1=="n" or answer1=="N":
					return main()
				elif answer1=="y" or answer1=="Y":
					return answer
		else:
			if os.path.exists(answer) and  answer[5:-1]=="sd" and answer[-1]=="a":
				return welcome("Error! Cant Use /dev/sda ,Please Enter Right USB FLash Memory Directory.")
			return welcome("Error! Enter Right USB FLash Memory Directory.")

def fix_flash(directory):
	nn="100%"
	for n in range(1,4):
		subprocess.call("umount -R $(findmnt %s%s  -n -o TARGET)  &>/dev/null"%(directory,str(n)),shell=True)
	check=subprocess.call("eject %s"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Eject %s"%directory)
	check=subprocess.call("eject -t %s"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Ansert %s"%directory)
		
	check=subprocess.call("parted %s mktable msdos"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Make Parttions Table For %s"%directory)
		
		
	check=subprocess.call("eject %s"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Eject %s"%directory)
	check=subprocess.call("eject -t %s"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Ansert %s"%directory)
		
		
	check=subprocess.call("parted %s mkpart primary fat32 1M %s"%(directory,nn),shell=True)
	if check!=0:
		return welcome("Error! Cant Make Parttion For %s"%directory)
		
		
	check=subprocess.call("eject %s"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Eject %s"%directory)
	check=subprocess.call("eject -t %s"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Ansert %s"%directory)
		
	for n in range(1,4):
		subprocess.call("umount -R $(findmnt %s%s  -n -o TARGET)  &>/dev/null"%(directory,str(n)),shell=True)
		
	check=subprocess.call("mkfs.vfat -F 32 %s1 -n FLASH"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Make Fat 32 File System For %s"%directory)
		

	check=subprocess.call("eject %s"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Eject %s"%directory)
	check=subprocess.call("eject -t %s"%directory,shell=True)
	if check!=0:
		return welcome("Error! Cant Ansert %s"%directory)
		
	sys.exit("\nFinish Bye...\n")

def main():
	fix_flash(welcome())


if __name__ == '__main__':
    sys.exit(main())
