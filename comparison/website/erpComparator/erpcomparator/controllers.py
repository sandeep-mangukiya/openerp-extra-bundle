
import turbogears as tg
from turbogears import controllers, expose
from turbogears import config

import cherrypy

from erpcomparator import rpc
from erpcomparator import common
from erpcomparator import stdvars
from erpcomparator import subcontrollers

host = config.get('host', path="erpcomparator")
port = config.get('port', path="erpcomparator")
protocol = config.get('protocol', path="erpcomparator")

database = config.get('database', path="admin")
user_name = config.get('user_name', path="admin")
password = config.get('password', path="admin")

rpc.session = rpc.RPCSession(host, port, protocol, storage=cherrypy.session)

class Root(controllers.RootController):
    @expose(template="erpcomparator.templates.index")
    def index(self):
        
        res = rpc.session.login(database, user_name, password)
        userinfo = cherrypy.session.get('user_info', '')
        
        return dict(userinfo=userinfo)

    comparison = subcontrollers.comparison.Comparison()
    softwares = subcontrollers.softwares.Softwares()
    about = subcontrollers.about.About()
    login = subcontrollers.login.Login()
    graph = subcontrollers.graph.Graph()
    