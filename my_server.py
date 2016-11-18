import socket
import time
import signal

class Server:
	"""docstring for server"""
	def __init__(self, port):
		super(Server, self).__init__()
		self.port = port 	# Define given port
		self.host = ''		# This '' means all the active interfaces
		self.host_dir = '2014IS064' 	# Web page store in here

	def run(self):
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			self.socket.bind((self.host,self.port))
			print('HTTP Server Running on H:',self.host,' P:',self.port)

		except Exception as e:
			print('Sorry! , PORT:',self.port,' already in use. Please try another port')
			import sys
			sys.exit(1)
		print('Server waiting to requests...')
		print('-'*60)
		self.get_connection()

	def header_gen(self,status):
		# Generate header for response

		#idetify status 
		head = ''
		if(status == 200):
			head = 'HTTP/1.1 200 OK\n'
		elif(status == 404):
			head = 'HTTP/1.1 404 Not Found\n'


		if self.req_file.endswith(".html"):
			mimetype='text/html'
		elif self.req_file.endswith(".jpg"):
			mimetype='image/jpg'
		elif self.req_file.endswith(".gif"):
			mimetype='image/gif'
		elif self.req_file.endswith(".js"):
			mimetype='application/javascript'
		elif self.req_file.endswith(".css"):
			mimetype='text/css'
		else:
			mimetype='text/html'

		# Additional header content
		date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		head += 'Date: '+ date +'\n'
		head += 'Server: Emalsha\'s-simple-HTTP-server\n'
		head += 'Content-Type: '+str(mimetype)+'\n'
		head += 'Connection: Close\n\n'

		return head

	def get_connection(self):
		# Loop to get connections
		while True:
			self.socket.listen(1) # Set number of queued connection  

			conn, addr = self.socket.accept() 
			#conn => Connected socket to client
			#addr => Client address

			print('Client connected on ',addr)

			request = conn.recv(1024).decode('utf-8') # get request data from client 

			temp = request.split(' ') 	# Split requset from spaces

			if len(temp) < 1:
				print('Request not valid')
				print('-'*60)
				print(request)
				conn.close()


			method = temp[0]
			req_file = temp[1]
			self.req_file = req_file

			print('Client requset ',req_file,' using ',method,' method')

			if (method == 'GET'):

				r_file = req_file.split('?')[0] # After the "?" symbol not relevent here
				if(r_file == '/'):
					r_file = '/index.html'	# Load index file as default

				request_file = self.host_dir+r_file # Modify requesting file

				# Read file 
				try:
					file = open(request_file,'rb') # open file , r => read , b => byte format
					response = file.read()
					file.close()

					header = self.header_gen(200) # Generate hearder
				except Exception as e:
					print('File not found ',request_file)
					header = self.header_gen(404)
					response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
				
				final_res = header.encode('utf-8')
				final_res += response

				conn.send(final_res)
				print('Close connection with client')
				print('-'*60)
				conn.close()

			else:
				print('HTTP request not valid. You used ',method)
				print('-'*60)

			conn.close()

print('-'*60)
print(' '*5,'# Author : Emalsha Rasad')
print(' '*5,'# Reg.No : 2014/IS/064')
print(' '*5,'# Instructions : This server serve files from folder \'2014IS064\'. Please create a folder manualy on this script store place. Then you can call files and images contain on it.')
print('-'*60)
print(' '*24,'Server start')
print('-'*60)
svr = Server(8081)
svr.run()


#HOST,PORT = '127.0.0.1',8082 # host -> socket.gethostname() use to set machine IP

#my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#my_socket.bind((HOST,PORT))
#my_socket.listen(1)

#print('Serving on port ',PORT)

#while True:
#    cl_conn,cl_addr = my_socket.accept()
#    req = cl_conn.recv(1024).decode('utf-8')
#    reqs = req.split(' ')
#    method = reqs[0]
#    req_file = reqs[1]

#    print('User want ',method,' file ',req_file)
    
    #cl_conn.sendall(http_res.encode('utf-8'))
    #print(http_res.encode('utf-8'))
    #cl_conn.sendfile('test.html');

    # with open('test.html','rb') as f:
    # 	cl_conn.send('HTTP/1.1 200 OK\n'.encode('utf-8'))
    # 	cl_conn.send('Content-Type: text/html\n'.encode('utf-8'))
    # 	cl_conn.send('Server: Emalsha-server/1.0\n\n'.encode('utf-8'))
    # 	for data in f:
    # 		cl_conn.sendall(data)

    # cl_conn.close()
