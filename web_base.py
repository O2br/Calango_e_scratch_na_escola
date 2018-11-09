import sys

if (sys.platform == 'esp8266'):
    import utime as time
    import usocket as socket
    import ure
else:
    import time  
    import socket
    import re as ure

    
html = """<!DOCTYPE html>
<html>
<head>
<title>Web Base</title>
</head>
    <body>
	<h1>Web Base - GET</h1>
		</p> 
	</body>
</html>
"""
ctypeDict = {}
ctypeDict[".htm"] = "text/html"
ctypeDict[".html"] = "text/html"
ctypeDict[".css"] = "text/css"
ctypeDict[".xml"] = "application/xml"
ctypeDict[".js"] = "application/javascript"
ctypeDict[".json"] = "application/json"

def parseURL(url):
    #PARSE THE URL AND RETURN THE PATH AND GET PARAMETERS
    parameters = {} 
    path = ure.search("(.*?)(\?|$)", url)   
    while True:
        vars = ure.search("(([a-z0-9]+)=([a-z0-8.]*))&?", url)
        if vars:
            parameters[vars.group(2)] = vars.group(3)
            url = url.replace(vars.group(0), '')
        else:
            break
    return path.group(1), parameters

def buildResponse(response):
    # BUILD DE HTTP RESPONSE HEADERS
    global html
    return '''HTTP/1.0 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s''' % (len(html), html)



def main():
    print("Oii")
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address: {}  socket: {} ".format(client_addr, client_sock))
        client_stream = client_sock.makefile("rwb")        
        print("HEAD:")
        obj = None
        objHost = None
        while True:
            request = client_stream.readline()
            if not obj:
                obj = ure.search("GET (.*?) HTTP\/1\.1", request.decode())                        
            if not objHost:
                objHost = ure.search("Host: (.*?)\r\n", request.decode())                        
            else:
                print(objHost)
            if request == b"" or request == b"\r\n":
                break
            print(request)  
           
        if not obj:
            print("INVALID REQUEST - GET")
        else:
            #print(" REGEX: {}  ".format(obj.group(1)))
            path, parameters = parseURL(obj.group(1))
            print("path: {}  parameters: {} ".format(path,parameters))                                                         
            if (ure.search('^\/(.+\.(css|xml|js|html|json))$', path)):                    
                global ctypeDict
                try:
                    arq_html = open(".{}".format(path)).read()
                    arq_html = ure.sub("\{\[host\]\}","http://{}".format(objHost.group(1)),arq_html)
                    html = '''HTTP/1.0 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-type: %s\r\nContent-length: %d\r\n\r\n%s''' % ( ctypeDict[path[path.index('.'):]],len(arq_html), arq_html)                                                            
                    client_stream.write(html.encode())                        
                except Exception as e:
                    client_stream.write( buildResponse("").encode())                                                                                
            elif path.startswith("/home"):
                print("rota /")
                client_stream.write( buildResponse("").encode())
            elif path.startswith("/halt"):
                print("rota /halt")
                client_stream.write(buildResponse("Shutting down server\n").encode())
                client_stream.close()
                client_sock.close()
                s.close()
                break
            else:
                print("Rota desconhecida  %s -> %s" % (path, parameters))
                client_stream.write(buildResponse("UNREGISTERED ACTION\r\nPATH: %s\r\nPARAMETERS: %s" % (path, parameters)).encode())                                             
        client_stream.close()            
        client_sock.close()
        
        print()
main()

