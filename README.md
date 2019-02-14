This python program uses PyNaCl library to encrypt/decrypt files using assymetric keys. 

This is the first release. It currently does not validate input nor trap errors. TODO

The purpose is to provide a simplified method to encrypt files using a public key. The program is written to handle large files, they are processed in chunks. The chunks are encrypted and stored as individual lines in the resulting file. The resulting file is not compressed, so it is much larger than the source/unencrypted file. This program could be modified to stream encrypted chunks across a network. 

There is no support for keychains and the keys are anonymous. 

Commands:

```
# encrypt.py genkey
```

This command generates a new private and public keypair. It will prompt for the password, which can be nothing (press enter).

Note: A blake2 hash is calculated for the password. The first 32 characters (base64 chars) are used to encrypt the private key. This strategy ensures that any password will suffice, even a blank password, and the private key is always encrypted. However, truncating the hash increases the possibility of collisions. (But the encryption key complexity remains 32 base64 characters, regardless). 

example: 

```
# ./encrypt.py genkey
Enter Password:1234
private key: 994396b913d17ef36d2862a8a2c2acf71659fe26e13c0da01ad36a8b697ecb4da3ddc68ccb66b89669241cc11ee0d6ddd88b2efb3b839dcd067776e0122f553037aaa14c4a8f5615cff5b422d0909a5dc9754ae121ce257a0fb9c5b8e728dcab598ed590263115e1
public key: eb840c0f144395e9f6c88d88060ce032cd852584fa9af7cc7acb32883864aa77
```

Store the private key somewhere safe. There is no mechanism to 'reset the password', so don't forget the password.

```
# encrypt.py dec filename
```

This command decrypts the file identified by "filename". It will first prompt for the secret key, then the password to unlock the secret key, then the output filename.

example:
```
# ./encrypt.py dec test.txt.enc
Enter private key:994396b913d17ef36d2862a8a2c2acf71659fe26e13c0da01ad36a8b697ecb4da3ddc68ccb66b89669241cc11ee0d6ddd88b2efb3b839dcd067776e0122f553037aaa14c4a8f5615cff5b422d0909a5dc9754ae121ce257a0fb9c5b8e728dcab598ed590263115e1
Enter Password:1234
Enter output filename: gg
# cat gg
This is a test.
Have a nice day.
1234
1234
123
1
```

```
# encrypt.py pubkey filename
```

This command encrypts the file identified by "filename" using the public key "pubkey". The output file is "filename" with the extension ".enc" appended.

example:
```
#./encrypt.py eb840c0f144395e9f6c88d88060ce032cd852584fa9af7cc7acb32883864aa77 test.txt
# cat test.txt.enc
gvkpgBgCmiWsbwUMOAGxi5S3rNqCiE3V3In5hU7QInmQpFGDrKng7UZ+eGc6f5Zf1y8lvViCZXHJCmXPprxtiVuh81wCFTAXCvsD36hBRQWK11jXJBJxDDvI4y6oWWgrKPw=
```


