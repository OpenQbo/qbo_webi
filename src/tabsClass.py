import cherrypy

class TabClass:

    @cherrypy.expose
    def unload(self):
        return "OK"
    def set_language(self,lang):
        self.language=lang
