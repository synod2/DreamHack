from pwn import *

res = (asm('sub %al ,0x4'))
res += (4-len(res))*"\x00"

print(hex(u32(res)))