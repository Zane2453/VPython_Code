import tornado.ioloop
import tornado.web
import os
import config
import requests
import json

"""
project_iframe_reset={
    'p_id_1':'is_reset',
    'p_id_2':'is_reset'
    }
"""
# project_iframe_reset={}


def make_app():

    route = [
        (r"/", chooseProjectHandler),
        (r"/project/(?P<odm_name>.*)", projectHandler),
        (r"/rc/(?P<odm_name>.*)/(?P<p_id>.*)/(?P<odm_id>.*)/(?P<in_do_id>.*)", rcHandler),
        (r"/da/vp/py/(?P<vp_file_name>.*)", daHandler),
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
        self.render("choose_vp.html")

#todo check model name exist or not
class projectHandler(tornado.web.RequestHandler):
    def get(self, **kwargs):
        print(kwargs)
        odm_name = kwargs.get('odm_name')
        self.render("da/vp_index.html", odm_name=odm_name)

#todo check all param
class rcHandler(tornado.web.RequestHandler):
    def get(self, **kwargs):
        print(kwargs)
        odm_name = kwargs.get('odm_name')
        p_id = kwargs.get('p_id')
        odm_id = kwargs.get('odm_id')
        in_do_id = kwargs.get('in_do_id')

        #todo send post request (get_df_list_from_dm_id) to iottalk
        r = requests.post("http://140.113.215.18:7788/get_df_list_from_dm_id", data={'dm_id': odm_id})
        odf_list = tornado.escape.json_decode(r.text)
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


if __name__ == "__main__":
    app = make_app()
    app.listen(config.port)
    tornado.ioloop.IOLoop.current().start()