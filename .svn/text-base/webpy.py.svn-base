# -*- coding: UTF-8 -*
'''
Created on 2013-10-11

@author: RobinTang
'''

import web
import random
import time
render = web.template.render('templates/')
urls = (
	'/upload/(.*)', 'Upload',
	'/get/(.*)', 'Source',
	'.*', 'Upload'
)

g_kvdb = {}

def genkey(l=10):
    ss = 'abcdefghijklmnopqrstuvwxyz1234567890'
    tk = ''.join([random.choice(ss) for i in range(0, l)])
    return '%s_%s_key'%(int(time.time()), tk)

def get_header(s, default=''):
    '''Get request header'''
    try:
        v = web.ctx.env.get(s, default)
        if not v or len(v)==0:
            v = web.ctx.env[s] 
    except:
        v = default
    return v

image_suffixs = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
text_suffixs = ['heml', 'txt', 'log', 'ini', 'c', 'cpp', 'java']


class Index(object):
	def GET(self):
		return 'Big Storage!'

class Source(object):
	def GET(self, key=''):
		global g_kvdb
		etag = get_header('HTTP_IF_NONE_MATCH')
		if etag == key:
			raise web.notmodified()	

		if key in g_kvdb:
			attrs = g_kvdb[key]
			web.header('Content-Type', attrs['Content-Type'])
			web.header('ETag', key)
			web.header('Content-Disposition', 'filename="%s"'%attrs['filename'])
			return g_kvdb[attrs['storekey']]
		else:
			return 'no thing'
		
class Upload(object):

	def GET(self, key=''):
		return render.upload(key=key)

	def POST(self, refkey=''):
		global g_kvdb
		filetype = web.input(type='image').type
		key = genkey()
		attrs = {}
		thisfile = web.input(file={}).file
		filename = thisfile.filename
		if filename:
			suffix = filename[filename.rfind('.')+1:]
			if suffix in image_suffixs:
				# images file
				attrs['Content-Type'] = 'image/%s'%suffix
			elif suffix in text_suffixs:
				# text file
				attrs['Content-Type'] = 'text/%s'%suffix
			else:
				# binary file
				attrs['Content-Type'] = 'application/octet-stream'
			attrs['storekey'] = '%s_store'%key
			attrs['filename'] = filename
			attrs['suffix'] = suffix
			g_kvdb[attrs['storekey']] = thisfile.value
			g_kvdb[key] = attrs
			if refkey == 'new':
				return key
			else:
				raise web.seeother('/upload/%s'%key)
		else:
			return 'fail'

app = web.application(urls, globals())

if __name__ == "__main__":
	app.run()
