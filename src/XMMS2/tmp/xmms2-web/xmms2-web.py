#!/usr/bin/python
import cherrypy
from xmmsclient import sync, XMMSError, PLAYBACK_STATUS_PAUSE, PLAYBACK_STATUS_PLAY, PLAYBACK_STATUS_STOP
from Cheetah.Template import Template
from os import path, listdir, getenv

global_template = "templates/global.tmpl"

templates = {
	"playlist":"templates/playlist.tmpl",
	"fs":"templates/fs.tmpl",
	"info":"templates/info.tmpl",
	"collections.browse":"templates/coll_browse.tmpl",
	"collections.edit":"templates/coll_edit.tmpl",
	"forms.new_playlist":"templates/new_playlist.tmpl",
	"forms.new_collection":"templates/new_collection.tmpl",
}

extensions = {
		'pcm':('.wav','flac','.mp3','.ogg','.wma'),
		'syn':('.sid','.mid','.mod'),
		'pls':('.pls','.m3u','xspf')
	}

def urlreplace(s):
	return ''.join( map(lambda c: c in '''$-_.+!*'," <>%#&''' and '%%%02X'%ord(c) or c, s ) )

info_values = ['id','title','artist','album','url']

def get_coll_infos( c, coll, ns='Playlists', values=info_values ):
	 return dict([ (i['id'],i) for i in c.coll_query_infos( c.coll_get(coll,ns),values) ])

def get_current_info( c ):
	d = dict.fromkeys(info_values)
	d.update(dict([ (k,v) for (s,k),v in
			c.medialib_get_info( c.playback_current_id() ).iteritems()
		]))
	return d

def iterate_playlist(c,pl=None):
	if not pl:
		pl = c.playlist_current_active()
	info = get_coll_infos( c, pl )
	for n,i in enumerate( c.playlist_list_entries(pl) ):
		info[i]['n'] = n
		yield info[i]

class Control:
	def __init__(self,site):
		self.site = site
		self.redirect = site.redirect

	@cherrypy.expose
	def play(self):
		self.site.c.playback_start()
		self.redirect()

	@cherrypy.expose
	def pause(self):
		self.site.c.playback_pause()
		self.redirect()

	@cherrypy.expose
	def stop(self):
		self.site.c.playback_stop()

	@cherrypy.expose
	def add(self,id):
		self.site.c.playlist_add_id(int(id))
		self.redirect()

	@cherrypy.expose
	def next(self):
		self.site.c.playlist_set_next_rel(1)
		self.site.c.playback_tickle()
		self.redirect()

	@cherrypy.expose
	def previous(self):
		self.site.c.playlist_set_next_rel(-1)
		self.site.c.playback_tickle()
		self.redirect()

	@cherrypy.expose
	def add(self,id):
		self.site.c.playlist_add_id(int(id))
		self.redirect()

class PlaylistControl:
	def __init__(self,site,playlist):
		self.site = site
		self.playlist = playlist
	def __call__(self,func,*args,**kwargs):
		try:
			f = getattr(self,func)
			if not f.exposed:
				raise cherrypy.NotFound()
		except AttributeError:
			raise cherrypy.NotFound()
		return f(*args,**kwargs)
	def redirect(self):
		self.site.redirect( '/playlist/'+self.playlist )

	@cherrypy.expose
	def load(self):
		if self.playlist != '_active':
			self.site.c.playlist_load( self.playlist )
		self.site.redirect()

	@cherrypy.expose
	def play(self,id):
		if self.playlist != '_active':
			self.site.c.playlist_load( self.playlist )
		self.site.c.playlist_set_next( int(id) )
		self.site.c.playback_tickle()
		self.site.c.playback_start()
		self.site.redirect()

	@cherrypy.expose
	def remove(self,id):
		self.site.c.playlist_remove_entry( int(id), self.playlist )
		self.redirect()

	@cherrypy.expose
	def move(self,src,dst):
		self.site.c.playlist_move( int(src), int(dst), self.playlist )
		self.redirect()

	@cherrypy.expose
	def delete(self):
		if self.playlist != '_active':
			self.site.c.playlist_remove( self.playlist )
		self.site.redirect()

	@cherrypy.expose
	def shuffle(self):
		self.site.c.playlist_shuffle( self.playlist )
		self.redirect()

	@cherrypy.expose
	def clear(self):
		self.site.c.playlist_clear( self.playlist )
		self.redirect()

class FS:
	def __init__(self,site):
		self.site = site
	def dict_from_args(self,*args):
		if '..' in args:
			raise cherrypy.NotFound()
		if args:
			a = path.join( *args )
		else:
			a = ''
		p = path.join( self.site.fsroot, a )
		return {
			'full_path': p,
			'mlib_path': 'file://'+p,
			'path_arguments': args,
			'path': a,
			'is_root': not args
			}

	@cherrypy.expose
	def list(self,*args):
		env = self.dict_from_args(*args)
		p = env['full_path'] 
		l = listdir( p )

		f = []
		for x in l:
			if path.isfile(path.join(p,x)):
				ext = x[-4:].lower()
				for type, e in extensions.items():
					if ext in e:
						f.append( ( x, type ) )
						break
		f.sort()
		env['files'] = f

		d = filter( lambda x:path.isdir(path.join(p,x)), l )
		d.sort()
		env['dirs'] = d
		return self.site.template('fs',env)

	@cherrypy.expose
	def info(self,*args):
		env = self.dict_from_args(*args)
		env['id'] = self.site.c.medialib_get_id( env['mlib_path'] )
		if env['id']:
			env['info'] = self.site.c.medialib_get_info( env['id'] )
		return self.site.template('info',env)

	@cherrypy.expose
	def libimport(self,*args):
		self.site.c.medialib_add_entry( self.dict_from_args(*args)['mlib_path'] )
		self.site.redirect( path.join( '/fs/list/', *args[:-1] ) )

	@cherrypy.expose
	def rimport(self,*args):
		self.site.c.medialib_path_import( self.dict_from_args(*args)['mlib_path'] )
		self.site.redirect( path.join( '/fs/list/', *args[:-1] ) )

	@cherrypy.expose
	def add(self,*args):
		self.site.c.playlist_add_url( self.dict_from_args(*args)['mlib_path'] )
		self.site.redirect()

	@cherrypy.expose
	def radd(self,*args):
		self.site.c.playlist_radd( self.dict_from_args(*args)['mlib_path'] )
		self.site.redirect()

class Collections:
	def __init__(self,site):
		self.site = site
	@cherrypy.expose
	def browse(self,coll):
		return self.site.template("collections.browse",{
			'coll_items': self.site.c.coll_query_infos(
				self.site.c.coll_get(coll,"Collections"), info_values ),
			'collection': coll
		})
	
	@cherrypy.expose
	def delete(self,coll):
		self.site.c.coll_remove(coll,"Collections")
		self.site.redirect()

	@cherrypy.expose
	def edit(self,coll):
		return self.site.template("collections.edit",{'name':coll,'collection':self.site.c.coll_get(coll,"Collections")})

#	@cherrypy.expose
#	def add(self,coll):
#		self.site.c.playlist_add_collection(coll,order) #TODO: find ordering
#		self.site.redirect()

class Site:
	def __init__(self):
		self.c = sync.XMMSSync("Web")
		self.c.connect(getenv("XMMS_PATH"))

		self.fsroot = '/home/ccx/audio'

		self.control = Control(self)
		self.fs = FS(self)
		self.coll = Collections(self)

		self.dict = {
				"root":"",
				"urlreplace":urlreplace,
				"PAUSE":PLAYBACK_STATUS_PAUSE,
				"PLAY":PLAYBACK_STATUS_PLAY,
				"STOP":PLAYBACK_STATUS_STOP
				}

	def redirect(self,path='/'):
		raise cherrypy.HTTPRedirect( self.dict['root']+path )

	def searchList(self):
		l = {
				'playlists': filter( lambda s: not s.startswith('_'), self.c.playlist_list()),
				'collections': self.c.coll_list('Collections'),
				'status_id': self.c.playback_status(),
				'active_playlist': self.c.playlist_current_active(),
				}
		l['status'] = {
				PLAYBACK_STATUS_PAUSE:'paused',
				PLAYBACK_STATUS_PLAY:'playing',
				PLAYBACK_STATUS_STOP:'stopped'
				}[ l['status_id'] ]
		if l['status_id'] != PLAYBACK_STATUS_STOP:
			l['current'] = get_current_info( self.c )
			try:
				l['playlist_pos'] = self.c.playlist_current_pos()
			except XMMSError:
				l['playlist_pos'] = -1
		return l

	def template(self,name,env={}):
		l = [
			{'content':templates[name]},
			env,
			self.searchList(),
			self.dict,
		] 
		return str( Template( file=global_template, searchList=l ) )

	@cherrypy.expose
	def index(self):
		return self.playlist( '_active' )

	@cherrypy.expose
	def forms(self,name):
		return self.template("forms."+name)

	@cherrypy.expose
	def info(self,id):
		return self.template('info',{ 
			'info':self.c.medialib_get_info( int(id) ), 
			'id': int(id)
		})

	@cherrypy.expose
	def playlist(self,name,*args,**kwargs):
		if args:
			return PlaylistControl(self,name)(*args,**kwargs)
		l = {
				"playlist": name,
				"playlist_items": tuple( iterate_playlist( self.c, name ) )
		}
		l.update( self.searchList() )
		if name=='_active' or name==l['active_playlist']:
			l["playlist_is_active"] = True
			l['playlist'] = l['active_playlist']
		else:
			l["playlist_is_active"] = False


		return self.template('playlist',l)

	@cherrypy.expose
	def new_playlist(self,name):
		self.c.playlist_create(name)
		self.redirect('/playlist/%s/'%name)


#cherrypy.config.update({
#	'tools.encode.on':'True',
#	'tools.encode.encoding':'utf-8'
#	})

cherrypy.quickstart( Site(), config='cherrypy.conf' )

