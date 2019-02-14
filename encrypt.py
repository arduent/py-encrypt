#!/usr/bin/env python
import sys
import getpass
import argparse
import nacl.utils
import nacl.encoding
import nacl.hash
import nacl.secret
import base64

from nacl.public import PrivateKey, SealedBox

def bytes_from_file(filename, chunksize=8192):
	with open(filename, "rb") as f:
		while True:
			chunk = f.read(chunksize)
			if chunk:
				yield chunk
			else:
				break

if len(sys.argv)<2:
	print('Usage: encrypt.py dec filename')
	print('Usage: encrypt.py pubkey filename [--chunksize=8192]')
	exit('Usage: encrypt.py genkey')

if sys.argv[1]=='genkey':
	pwd = str.encode(getpass.getpass("Enter Password:"))
	HASHER = nacl.hash.blake2b
	digest = HASHER(pwd, encoder=nacl.encoding.Base64Encoder)
	key = digest[0:nacl.secret.SecretBox.KEY_SIZE]
	skey = PrivateKey.generate()
	pkey = skey.public_key
	box = nacl.secret.SecretBox(key)
	encskey = box.encrypt(skey.encode(encoder=nacl.encoding.HexEncoder))
	print ("private key:",encskey.hex())
	print ("public key:",pkey.encode(encoder=nacl.encoding.HexEncoder).decode('utf-8'))
	exit()

if len(sys.argv)<3:
	print('Usage: encrypt.py genkey')
	print('Usage: encrypt.py dec filename')
	exit('Usage: encrypt.py pubkey filename [--chunksize=8192]')

if sys.argv[1]=='dec':
	chkkey = getpass.getpass("Enter private key:")
	pwd = str.encode(getpass.getpass("Enter Password:"))
	HASHER = nacl.hash.blake2b
	digest = HASHER(pwd, encoder=nacl.encoding.Base64Encoder)
	key = digest[0:nacl.secret.SecretBox.KEY_SIZE]
	box = nacl.secret.SecretBox(key)
	chkprivate = box.decrypt(bytes.fromhex(chkkey))
	skey = PrivateKey(chkprivate, encoder=nacl.encoding.HexEncoder)
	enc = SealedBox(skey)
	chkfile = input("Enter output filename: ")
	fout = open(chkfile,'wb')
	fin = open(sys.argv[2],'r')
	for line in fin:
		if len(line)>2:
			line = line.rstrip("\n")
			ln = base64.b64decode(line)
			dec = enc.decrypt(ln)
			#sys.stdout.buffer.write(dec)
			fout.write(dec)
	fout.close()
	fin.close()
	exit()

parser = argparse.ArgumentParser(description='Encrypt/Decrypt file.')
parser.add_argument('strings', metavar='N', nargs='+')
parser.add_argument('--chunksize', action='store', dest='chunksize', type=int, default=8192,required=False)
args=parser.parse_args()
chunksize=args.chunksize

if len(sys.argv[1])!=64:
	exit('Invalid public key')

pkey = nacl.public.PublicKey(sys.argv[1], encoder=nacl.encoding.HexEncoder)
enc = SealedBox(pkey)

fout = open(sys.argv[2]+'.enc', 'wb')
for b in bytes_from_file(sys.argv[2],chunksize):
	fout.write(base64.b64encode(enc.encrypt(b)))
	fout.write(b'\n')

fout.close()

