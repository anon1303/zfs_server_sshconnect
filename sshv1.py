# from paramiko import SSHClient, AutoAddPolicy
import paramiko
from getpass import getpass

def get_data():

	#LOAD HOST KEYS
	client = paramiko.SSHClient()

	client.load_host_keys('C:/Users/Excomnunicado/.ssh/id_rsa')
	# ssh_key = 'C:/Users/Excomnunicado/.ssh/id_rsa'
	# ssh = paramiko.RSAKey.from_private_key_file(ssh_key)

	# client.look_for_keys(True)
	client.load_system_host_keys()

	#Known_host policy
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	host = '147.182.255.222' #Change this into the ipaddress of the machine you want to connect

	# password = getpass('Enter password :')
	# client.connect()

	client.connect(hostname = host,
					username='root',
					# key_filename = ssh
					# password = password
					)
	# client.connect('192.168.0.109', username='root')


	# client.exec_command('hostname')
	stdin, stdout, stderr = client.exec_command('/tools/samplecode.py', get_pty=True)
	print(type(stdin))
	print(type(stdout))
	print(type(stderr))
	for line in iter(stdout.readline, ""):
		print(line, end="")

	# # Optionally, send data via STDIN, and shutdown when done
	# stdin.write('Hello world')
	# stdin.channel.shutdown_write()

	# # Print output of command. Will wait for command to finish.
	print(f'STDOUT: {stdout.read().decode("utf8")}')
	print(f'STDERR: {stderr.read().decode("utf8")}')

	# # Get return code from command (0 is default for success)
	print(f'Return code: {stdout.channel.recv_exit_status()}')

	# # Because they are file objects, they need to be closed
	stdin.close()
	stdout.close()
	stderr.close()

	# # Close the client itself
	client.close()

def main():

	get_data()



if __name__ == '__main__':
	try:
		# ARGS = get_args()

		main()
	except KeyboardInterrupt:
		print('\nReceived Ctrl^C. Exiting....')
	except Exception:
	    ETRACE = traceback.format_exc()
	    print(ETRACE)