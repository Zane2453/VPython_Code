import tornado.ioloop
import tornado.web
import os
import requests
import json
import math
import sys

import config
import project_manage

"""
project_iframe_reset={
    'p_id_1':'is_reset',
    'p_id_2':'is_reset'
    }
"""
# project_iframe_reset={}

vp_list = ['Ball-throw2', 'Precession', 'Snakepend', 'Universe']


def make_app():

    route = [
        (r"/", chooseProjectHandler),
        (r"/project/(?P<odm_name>.*)", projectHandler),
        (r"/rc/(?P<odm_name>.*)/(?P<p_id>.*)/(?P<odm_id>.*)/(?P<in_do_id>.*)", rcHandler),
        (r"/da/vp/py/(?P<vp_file_name>.*)", daHandler),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {'path': './vp/image'}),
        (r"/audio/(.*)", tornado.web.StaticFileHandler, {'path': './vp/audio'}),
        (r"/delete_project/(?P<p_id>.*)", deleteProjectHandler),
    ]

    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    
    return tornado.web.Application(route, **settings)

'''
class choose_vp_handler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
    def post(self):
        self.write("hhhhh")
    # def delete():
    #     self.write("hhhhh")
    # def put():
    #     self.write("hhhhh")
    # def option():
    #     self.write("hhhhh")
'''

class chooseProjectHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main_page.html")

class projectHandler(tornado.web.RequestHandler):
    def get(self, **kwargs):
        print(kwargs)
        odm_name = kwargs.get('odm_name')
        if odm_name in vp_list:
            cur_p_id = project_manage.create_project_handler(odm_name)
            project_info = project_manage.project_set[cur_p_id]
            #TODO save out dm_name
            url = config.iottalk_ip + ":"+ str(config.port) + "/rc/"+ project_info['output_device_info']['dm_name'] + "/" +str(cur_p_id)+\
            "/"+str(project_info['output_device_info']['dm_id'])+\
            "/"+str(project_info['input_device_info']['do_id'])
            self.render("da/vp_index.html", p_id=cur_p_id, odm_name=odm_name, url=url, odo_id=project_info['output_device_info']['do_id'])
        else:
            self.redirect('/')

#todo check all param
class rcHandler(tornado.web.RequestHandler):
    def get(self, **kwargs):
        odm_name = kwargs.get('odm_name')
        p_id = kwargs.get('p_id')
        odm_id = kwargs.get('odm_id')
        in_do_id = kwargs.get('in_do_id')

        r = requests.post(config.iottalk_ip+":"+config.ccm_port+"/get_df_list_from_dm_id", data={'dm_id': odm_id})
        odf_list = tornado.escape.json_decode(r.text)
        print('odf_list: ',odf_list)
        self.render("da/mobile_rc.html", odm_name=odm_name, p_id=p_id, in_do_id=in_do_id, odf_list=odf_list)

class daHandler(tornado.web.RequestHandler):
    def get(self, **kwargs):
        vp_file_name = kwargs.get('vp_file_name')
        no_cache_headers = {
            'Cache-Control': ('no-store, no-cache, must-revalidate, '
                              'post-check=0, pre-check=0, max-age=0'),
            'Pragma': 'no-cache',
            'Expires': '-1',
        }
        for key, val in no_cache_headers.items():
            self.set_header(key, val)

        f = open(os.path.join(os.getcwd(), "vp/py/"+vp_file_name), "r")
        self.write(f.read())

class deleteProjectHandler(tornado.web.RequestHandler):
    def delete(self, **kwargs):
        p_id = kwargs.get('p_id')
        print('delete_project p_id=',p_id)
        project_manage.delete_project_handler(p_id)
        self.write('ok')

def stop_tornado():
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.add_callback(ioloop.stop)
    print("Asked Tornado to exit")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == 'stop':
            stop_tornado()
    app = make_app()
    app.listen(config.port)
    tornado.ioloop.IOLoop.current().start()