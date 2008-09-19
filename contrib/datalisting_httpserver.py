"""
Starts a webserver on a specified host and port that lists all the available pygr.Data 
resources as a hierarchical tree.

Usage:

run the module on its own or execute the module level function with the signature:

start_server(host='localhost', port=8080)

$Rev$ 
$Author$ 
$Date$
"""
import sys
import pygr.Data
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def info( msg, stream=sys.stdout ):
    "A logging function that prints messages to a stream"
    stream.write( 'INFO: %s\n' % msg)
    stream.flush()

def human_bytes( value ):
    """
    Returns a size as human readable bytes
    
    >>> human_bytes(100), human_bytes(10**4), human_bytes(10**8), human_bytes(10**10)
    ('100 bytes', '9 Kbytes', '95 Mbytes', '9 Gbytes')
    """
    if value < 1024: return "%s bytes" % value
    elif value < 1048576: return "%s Kbytes" % int(value/1024)
    elif value < 1073741824: return "%s Mbytes" % int(value/1048576)
    else: return "%s Gbytes" % int(value/1073741824)

class RequestHandler(BaseHTTPRequestHandler):

    def mime_headers(self, code=200, mimetype="text/html"):
        "Sets server headers"
        self.send_response(code)
        self.send_header('Content-type', mimetype )
        self.end_headers()   

    def write(self, msg):
        "Write to the return page"
        self.wfile.write( str(msg) )

    def do_GET(self):
        try:
            self.mime_headers()            
            page = html_page()            
            self.write( page )
        except Exception, exc:
            self.send_error(500,'%s' % exc)

class Leaf( object ):
    "Represents an end node of the tree"
    def __init__(self, name, attrs):
        self.name = name
        self.size = human_bytes (attrs['pickle_size'])
        self.doc  = attrs['__doc__']

    def render(self, depth):
        "Renders a node as html"
        shift = '\t'* depth 
        tags = [ '<div class="leaf">%(name)s' % self.__dict__ ]
        tags.append( '\t<div class="doc">%(doc)s</div>' % self.__dict__ )
        tags.append( '\t<div class="doc">Size=%(size)s</div>' % self.__dict__ )
        tags.append( '</div>' )
        tags = [ shift + t for t in tags ]
        return '\n'.join(tags) 

class Tree(object):
    "Represents a tree and allows it to be rendered as HTML"
    def __init__(self):
        self.root = {}
        self.leafcount = 0

    def build( self, data ):
        """
        Builds a tree based on pygr.Data.dir('', asDict=True) type dictionary

        """
        
        # will extract the hierarchy from the dot separated fields
        for fields, values in data.items():
            base  = self.root
            elems = fields.split('.') + [ None ]
            for name, next in zip(elems, elems[1:]):
                if name not in base:
                    if next is None:
                        base[name] = Leaf( name=name, attrs=values )
                        self.leafcount += 1
                    else:    
                        base[name] = {}
                base = base[name]
        
    def render( self, root=None, depth=0, out=None):
        "Renders the tree as HTML"
        root = root or self.root
        out  = out or []
        shift = '\t' * depth # makes it look nicer in plaintext
        for name, node in root.items():
            if isinstance(node, Leaf):   
                out.append( node.render( depth=depth ) )
            else:
                out.append( shift + '<div class="node">%s' % name )
                self.render( root=node, depth=depth+1, out=out )  
                out.append( shift + "</div>" ) 
        return out
    
def html_page():
    "Builds the HTML page that will be returned"
    
    reload( pygr.Data )

    data = pygr.Data.dir('', asDict=True)

    tree = Tree()
    tree.build( data )
    found = tree.leafcount

    page = []
    page.append("<html><head>")
    page.append("""
    <style type="text/css"> 
        body  { font-family: arial  }
        .node { padding-left: 50px; font-weight:bold; font-family: arial  }
        .leaf { padding-left: 50px; }
        .doc  { padding-left: 50px; font-weight:normal;}
    </style>
    """)
    page.append("</head>")
    page.append("<h2>pygr.Data resource listing: found %s resources</h2>" % found)
    
    page.extend( tree.render() )
    page.append("</body></html>")
    
    return '\n'.join(page)

def server_start(host='localhost', port=8080):
    """
    Starts a HTTP server on the host and port specified as parameters
    The server will list the available pygr.Data entities
    """
    try:
        server = HTTPServer((host, port), RequestHandler)
        info("starting httpserver on '%s:%s'"  % (host, port) )
        server.serve_forever()
    except KeyboardInterrupt:
        inf( '^C received, shutting down server' )
        server.socket.close()
    
if __name__ == '__main__':
    
    #print html_page()

    server_start(host='localhost', port=8080)
    