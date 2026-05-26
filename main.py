import socket

HOST = "0.0.0.0"
PORT = 8000

server = socket.socket()
server.bind((HOST, PORT))# host and port la server ha atach panuthu
server.listen(5)# upto 5 clients can connect to this server

print(f"Server running at http://localhost:{PORT}")# printing the port number with server running

while True:
    client, addr = server.accept() # accept a new client connection
    request = client.recv(1024).decode()# recieving client request.

    print(request)  

    try:
        firstLine = request.split("\n")[0] # get first line of HTTP request
        parts = firstLine.split(" ") # split method, path, HTTP version

        method = parts[0]  # HTTP method (GET, POST, etc.)
        path = parts[1] # requested URL path
    except:
        client.close()
        continue

    # allowing GET method only
    if method != "GET":
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nOnly GET supported"
        client.send(response.encode()) # send error response
        client.close() # close connection
        continue # skip rest of code

    # mapping URL paths to files
    print("path -->>>", path) # print requested path
    if path == "/":
        fileName = "index.html"# home page, landing,first page
    elif path == "/style.css":
        fileName = "style.css"
    elif path == "/profile":
        fileName = "nelofer.png"
    elif path == "/bio.html":      
        fileName = "bio.html"
    elif path == "/hobby.html":      
        fileName = "hobby.html"
    elif path == "/education.html":  
        fileName = "education.html"
    elif path == "/ambition.html":   
        fileName = "ambition.html"
    else:
        fileName = None # invalid path

    # response
    if fileName:
        try:
            # if file is image
            if fileName.endswith(".png"):
                file = open(fileName, "rb") # open image in binary mode
                body = file.read() # read image data
                file.close() # close the image file

                response = b"HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n" + body

            # if file is css
            elif fileName.endswith(".css"):
                file = open(fileName) # open css file
                body = file.read() # read file
                file.close() # close the css file

                response = ("HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n" + body).encode()

            # if file is html
            else:
                file = open(fileName) # open html file
                body = file.read() # read file
                file.close() # close the html file

                response = ("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + body).encode()

        except:
            # if file not found or error occurs
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found".encode()
    else:
        # if path does not match any file
        response = "HTTP/1.1 404 Not Found\r\n\r\nPage not found".encode()

    client.send(response) # send response to browser/client
    client.close() # close client connection