#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse, parse_qs


class smcHandler(BaseHTTPRequestHandler):
    
    def template_index(self, data):
        html='<html><head></head><body></body></html>'
        return html

    def template_video(self, data):
        html='<html><head><link href="http://vjs.zencdn.net/5.11.9/video-js.css" rel="stylesheet"><script src="http://vjs.zencdn.net/ie8/1.1.2/videojs-ie8.min.js"></script></head><body><video id="my-video" class="video-js" controls preload="auto" width="640" height="264" poster="MY_VIDEO_POSTER.jpg" data-setup=""><source src="http://127.0.0.1:8080/{0}" type="video/mp4"><p class="vjs-no-js">HTML5 is required!</p></video><script src="http://vjs.zencdn.net/5.11.9/video.js"></script></body></html>'.format(data['video'][0])
        return html

    def get_template(self, name, data):
        if 'video' in name:
            html = self.template_video(data)
        else:
            html = self.template_index(data)
        return html


    def parse_url(self, url):
        return parse_qs(urlparse(url).query)

    def do_GET(self):
        request = self.parse_url(self.path)
        if 'video' in request:
            viewTemplate = self.get_template('video', request)
        else:
            viewTemplate = self.get_template('index', request)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(viewTemplate)
        return


class SMC:

    PORT = 8080
    def __init__(self, PORT=None):
        if PORT:
            self.PORT = PORT

    def run(self):
        try:
            server = HTTPServer(('', int(self.PORT)), smcHandler)
            print 'Started SmallMediaCenter on port: {0} '.format(self.PORT)
            server.serve_forever()

        except KeyboardInterrupt:
            print 'Shutting down the SmallMediaCenter...'
            server.socket.close()

if __name__ == "__main__":
    smc = SMC()
    smc.run()