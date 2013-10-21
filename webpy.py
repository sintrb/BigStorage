# -*- coding: UTF-8 -*
'''
Created on 2013-10-11

@author: RobinTang
'''

import web
import random
import time
from SinKVDB import SinKVDB
from dbbase import get_connect

render = web.template.render('templates/')
urls = (
	'/upload/(.*)', 'Upload',
	'/list/(.*)', 'List',
	'/get/(.*)', 'Source',
	'/(.*)', 'Upload',
	'.*', 'Upload'
)

def genkey(l=10):
	ss = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	tk = ''.join([random.choice(ss) for i in range(0, l)])
	return tk

def get_header(s, default=''):
	'''Get request header'''
	try:
		v = web.ctx.env.get(s, default)
		if not v or len(v) == 0:
			v = web.ctx.env[s] 
	except:
		v = default
	return v

image_suffixs = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
text_suffixs = ['heml', 'txt', 'log', 'ini', 'c', 'cpp', 'java']
class BaseClass():
	def __init__(self):
		self.kvdb = SinKVDB(dbcon=get_connect(), table='tb_bigstorage_key', tag='bs', reset=False, cache=True, cachesize=10, debug=False)
		self.kvdbval = SinKVDB(dbcon=get_connect(), table='tb_bigstorage_val', tag='bs', reset=False, cache=True, cachesize=10, debug=False)

class Source(BaseClass):
	def GET(self, key=''):
		etag = get_header('HTTP_IF_NONE_MATCH')
		if key in self.kvdb:
			if etag == key:
				raise web.notmodified()
			else:
				attrs = self.kvdb[key]
				if not 'viewcount' in attrs:
					attrs['viewcount'] = 0
				attrs['viewcount'] = attrs['viewcount']+1
				self.kvdb[key] = attrs
				web.header('View-Count', attrs['viewcount'])
				web.header('Content-Type', attrs['Content-Type'])
				web.header('ETag', key)
				web.header('Content-Disposition', 'filename="%s"' % attrs['filename'])
				return self.kvdbval[key]
		else:
			return 'no thing'
		
class Upload(BaseClass):
	def GET(self, key=''):
		return render.upload(key=key)

	def POST(self, refkey=''):
		keylen = 64
		key = genkey(keylen)
		while key in self.kvdb:
			key = genkey(keylen)
		attrs = {}
		thisfile = web.input(file={}).file
		filename = thisfile.filename
		if filename:
			suffix = filename[filename.rfind('.') + 1:]
			if suffix in image_suffixs:
				# images file
				attrs['Content-Type'] = 'image/%s' % suffix
			elif suffix in text_suffixs:
				# text file
				attrs['Content-Type'] = 'text/%s' % suffix
			else:
				# binary file
				attrs['Content-Type'] = 'application/octet-stream'
			attrs['filename'] = filename
			attrs['key'] = key
			attrs['time'] = int(time.time())
			attrs['suffix'] = suffix
			self.kvdb[key] = attrs

			self.kvdbval[key] = thisfile.value

			self.kvdb.commit()
			self.kvdbval.commit()

			if refkey == 'new':
				return key
			else:
				raise web.seeother('/%s' % key)
		else:
			return 'fail'


class List(BaseClass):
		def GET(self, oth=''):
			objs = self.kvdb.values()
			return render.filelist(objs=objs)

app = web.application(urls, globals())

if __name__ == "__main__":
	app.run()
