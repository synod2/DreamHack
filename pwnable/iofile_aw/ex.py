from pwn import *

p = process("./iofile_aw")

p.sendlineafter("#","read")
p.sendline("b"*10)
p.sendlineafter("#","")
# p.sendlineafter("#","a"*512)
p.interactive()