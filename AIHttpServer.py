# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Simple HTTP Server With Upload.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

see: https://gist.github.com/UniIsland/3346170
"""
 
 
__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
 
import os
import posixpath
import http.server
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import urllib.request, urllib.parse, urllib.error
import cgi
import shutil
import mimetypes
import re
from io import BytesIO
import json
import socket
import PIL
from PIL import Image
from ImageClassifier.AIModule import getShape
import numpy as np
from socketserver import ThreadingMixIn
import cgi
def GetIP():
    name = socket.getfqdn(socket.gethostname())
    addr = socket.gethostbyname(name)
    return name,addr
class AIServer(http.server.SimpleHTTPRequestHandler):
 
    """Simple HTTP request handler with GET/HEAD/POST commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method. And can reveive file uploaded
    by client.

    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.

    """
    mac_ip_dict = {}
    server_version = "SimpleHTTPWithUpload/" + __version__
 
    def do_GET(self):
        """Serve a GET request."""
        if (self.path == '/'):
            f = self.send_head()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
        elif self.path == '/getShapeJ':
            data = {'result':'this is a circle'}
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        elif self.path == '/getShape':
            self.path = "/"
            f = self.send_head()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
 
    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()
 
    def LoadJson(self):
        content_len = int(self.headers['Content-Length'])
        encode_json = self.rfile.read(content_len)
        decode_json = json.loads(encode_json)
        return decode_json
    def WriteJson(self,dict):
        jstr = json.dumps(dict)
        f = BytesIO()
        f.write(bytes(jstr, encoding = "utf8")  )
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def deal_formdata(self):
        form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST',
                    'CONTENT_TYPE':self.headers['Content-Type'],
                    }
        )

        image = None
        for field in form.keys():
            field_item = form[field]
            filename = field_item.filename
            filevalue  = field_item.value
            filesize = len(filevalue)

            
            byte_stream = BytesIO(filevalue);
            image = Image.open(byte_stream)
            
        return image

    def deal_formdata_(self):
        content_type = self.headers['Content-Type']
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        contents = content_type.split("=")

        if(len(contents) < 2):
                return (False, "Content-Type header size < 2")
        boundary = contents[1].encode()

        remainbytes = 9999999
        #remainbytes = int(self.headers['Content-Length'])
        
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)

        filedata = self.rfile.read();
        #filedata = self.rfile.read(remainbytes);

        byte_stream = BytesIO(filedata);
        image = Image.open(byte_stream)
        #image.show()
        return image

    def process(self):
        if(self.path == '/MACandLIP'):
            decode_json = self.LoadJson()
            self.mac_ip_dict[decode_json['MAC']] =decode_json['LIP']

            jdict = {'status': 'ok'}
            self.WriteJson(jdict)
            
        elif(self.path == '/MAC'):
            decode_json = self.LoadJson()
            mac = decode_json['MAC']
            
            jdict = {'MAC': '','LIP':''}
            jdict['MAC'] = mac;

            if mac in self.mac_ip_dict:
                jdict['LIP'] = self.mac_ip_dict[mac];

            self.WriteJson(jdict)
        elif(self.path == '/Image'):

            image = self.deal_formdata()


            jdict = {"category":"shape", "color":"0","shape":"xxx"}
            jdict['shape'] = getShape(np.asarray(image))
            #jdict = {"category":"letter","color":"xxx","letter","xxx"}
            #jdict = {"category":"number","color":"xxx","number","xxx"}
            #jdict = {"category":"fail"}
            self.WriteJson(jdict);
        else:
            r, info = self.deal_post_data()
            print((r, info, "by: ", self.client_address))
            f = BytesIO()
            f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
            f.write(b"<html>\n<title>Upload Result Page</title>\n")
            f.write(b"<body>\n<h2>Upload Result Page</h2>\n")
            f.write(b"<hr>\n")
            if r:
                f.write(b"<strong>Success:</strong>")
            else:
                f.write(b"<strong>Failed:</strong>")
            f.write(info.encode())
            f.write(("<br><a href=\"%s\">back</a>" % self.headers['referer']).encode())
            f.write(b"<hr><small>Powerd By: bones7456, check new version at ")
            f.write(b"<a href=\"http://li2z.cn/?s=SimpleHTTPServerWithUpload\">")
            f.write(b"here</a>.</small></body>\n</html>\n")
            length = f.tell()
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            if f:
                self.copyfile(f, self.wfile)
                f.close()
    def do_OPTIONS(self):
        self.process()
    def do_POST(self):
        """Serve a POST request."""
        self.process()
       
        
    def deal_post_data(self):
        content_type = self.headers['content-type']
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        contents = content_type.split("=")


        if(content_type == "application/json"):
            print('json')
            content_len = int(self.headers['Content-Length'])
            data = self.rfile.read(content_len)

            jstr = json.loads(data)
            print(jstr)
            return (True,"json ok")
        else:
            
            if(len(contents) < 2):
                return (False, "Content-Type header size < 2")
            boundary = [1].encode()
            remainbytes = int(self.headers['content-length'])
            line = self.rfile.readline()
            remainbytes -= len(line)
            if not boundary in line:
                return (False, "Content NOT begin with boundary")
            line = self.rfile.readline()
            remainbytes -= len(line)
            fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
            if not fn:
                return (False, "Can't find out file name...")
            path = self.translate_path(self.path)
            fn = os.path.join(path, fn[0])
            line = self.rfile.readline()
            remainbytes -= len(line)
            line = self.rfile.readline()
            remainbytes -= len(line)
            try:
                out = open(fn, 'wb')
            except IOError:
                return (False, "Can't create file to write, do you have permission to write?")
                
            preline = self.rfile.readline()
            remainbytes -= len(preline)
            while remainbytes > 0:
                line = self.rfile.readline()
                remainbytes -= len(line)
                if boundary in line:
                    preline = preline[0:-1]
                    if preline.endswith(b'\r'):
                        preline = preline[0:-1]
                    out.write(preline)
                    out.close()
                    return (True, "File '%s' upload success!" % fn)
                else:
                    out.write(preline)
                    preline = line
            return (False, "Unexpect Ends of data.")
 
    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f
 
    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = BytesIO()
        displaypath = cgi.escape(urllib.parse.unquote(self.path))
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(("<html>\n<title>Directory listing for %s</title>\n" % displaypath).encode())
        f.write(("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath).encode())
        f.write(b"<hr>\n")
        f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write(b"<input name=\"file\" type=\"file\"/>")
        f.write(b"<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write(b"<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write(('<li><a href="%s">%s</a>\n'
                    % (urllib.parse.quote(linkname), cgi.escape(displayname))).encode())
        f.write(b"</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f
 
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = [_f for _f in words if _f]
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path
 
    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)
 
    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
 
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']
 

        if not mimetypes.inited:
            mimetypes.init() # try to read system mime.types
        extensions_map = mimetypes.types_map.copy()
        extensions_map.update({
            '': 'application/octet-stream', # Default
            '.py': 'text/plain',
            '.c': 'text/plain',
            '.h': 'text/plain',
            })

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')
        SimpleHTTPRequestHandler.end_headers(self)
    
class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)
 
    
class ThreadingHttpServer( ThreadingMixIn,http.server.HTTPServer ):
    pass

def start_server():
    #http.server.test(HandlerClass, ServerClass)
    
    name ,addr = GetIP()
    host = ('0.0.0.0', 8888)
    server = ThreadingHttpServer(host, AIServer)
    print('Starting server, listen at: %s:%s' % host)
    server.serve_forever()
 
if __name__ == '__main__':
    start_server()   


