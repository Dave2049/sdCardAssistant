import ctypes
import os

def mount(source, target, fs,options=''):
	ret = ctypes.CDLL('libc.so.6', use_errno=True).mount(source, target, fs, 0, options)
	if(ret < 0):
		errno = ctypes.get_errno()
		raise RuntimeError('Error mounting')

mount('/dev/sdb1','mnt/sdCard','exfat','-o uid=pi,gid=pi')
