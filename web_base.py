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
ctypeDict[".ico"] = "image/x-icon"
ctypeDict[".png"] = "image/png"

def parseURL(url):
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
#    print("Oii")
    s = socket.socket()
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
        #print(type(client_stream))
        print("HEAD:")
        obj = None
        objHost = None
        
        while True:
            request = client_stream.readline()
            #print("Resultado Requisição:  {}".format(request))
            if not obj:
                obj = ure.search("GET (.*?) HTTP\/1\.1", request.decode())                        
            if not objHost:
                objHost = ure.search("Host: (.*?)\r\n", request.decode())                        
            if (request == b"\r\n" or request == b""):
                break                 
                
        if not obj:
            html = '''HTTP/1.0 404 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n''' 
            client_stream.write( html.encode())            
            #print("INVALID REQUEST - GET")
        else:
            #print(" REGEX: {}  ".format(obj.group(1)))
            path, parameters = parseURL(obj.group(1))
            print("path: {}  parameters: {} ".format(path,parameters))                                                         
            if (ure.search('^\/(.+\.(css|xml|js|html|htm|json|ico|png))$', path)):                    
                global ctypeDict
                try:
                    f = open(".{}".format(path),"rb")
                    arq_html = f.read()
                    f.close()
                    if (ure.search('^\/(.+\.(css|xml|js|html|htm|json))$', path)):
                        
                        arq_html = arq_html.decode().replace("{[host]}","http://{}".format(objHost.group(1)))
                        #if (sys.platform == 'esp8266'):
                        #    arq_html = arq_html.decode().replace("{[host]}","http://{}".format(objHost.group(1)))
                        #else:
                        #    arq_html = ure.sub("\{\[host\]\}","http://{}".format(objHost.group(1)),arq_html.decode())
                            
                            
                        html = '''HTTP/1.0 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-type: %s\r\nContent-length: %d\r\n\r\n%s''' % ( ctypeDict[path[path.index('.'):]],len(arq_html), arq_html)
                        client_stream.write(html.encode())     
                    else:
                        html = '''HTTP/1.0 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-type: %s\r\nContent-length: %d\r\n\r\n''' % ( ctypeDict[path[path.index('.'):]],len(arq_html))                                                                               
                        client_stream.write(html.encode())
                        client_stream.write(arq_html)
                        client_stream.close()
                        arq_html = None
                        html = None
                except Exception as e:
                    html = '''HTTP/1.0 404  Not Found\r\n\r\n<html><body><center><h3>Error 404: File not found</h3><p>ESP8266 HTTP Server</p></center></body></html>''' 
                    print(e)
                    client_stream.write(html.encode())                                                                                
            elif (path == "/"):
                print("Pagina inicial")
                client_stream.write( buildResponse("").encode())                    
            elif path.startswith("/api"):
                print("/api")
                html = '''HTTP/1.0 200 OK\r\nAccess-Control-Allow-Origin: *\r\n\r\n''' 
                client_stream.write( html.encode())            
                print("API")                
            elif path.startswith("/ana0"):
                print("rota /")
                html = '''HTTP/1.0 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-type: text/plain\r\nContent-length: %d\r\n\r\n%s''' % (len("12213.33"), "12213.33")
                client_stream.write( html.encode())                
            elif path.startswith("/halt"):
                print("rota /halt")
                client_stream.write(buildResponse("Shutting down server\n").encode())
                client_stream.close()
                client_sock.close()
                s.close()
                break
            else:
                
                html = '''HTTP/1.0 404  Not Found\r\n\r\n<html><body><center><h3>Error 404: File not found</h3><p>ESP8266 HTTP Server</p></center></body></html>''' 
                client_stream.write( html.encode())
                print("INVALID REQUEST - GET")
        
        client_stream.close()            
        client_sock.close()        
        print("-----------------------------------------------------")
    print("Finaliza a conexão socket")
    s.close()
        
main()