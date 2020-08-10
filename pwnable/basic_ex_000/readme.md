# basic ex 000
-------
```
Ubuntu 16.04
Arch:     i386-32-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX disabled
PIE:      No PIE (0x8048000)
RWX:      Has RWX segments
```

bof를 이용하여 쉘코드를 ret위치에 덮어쓰는 문제.

%s로 입력을 받기 때문에 \x09~\x0d 까지는 사용이 불가하다. 

execve의 시스템 콜 0x0b를 넣는 부분을 두단계로 나눈 쉘코드를 사용하면 된다. 

나같은 경우는 mov %al , 0x0b 를

mov %al , 0x0e
sub %al , 0x03

의 두단계로 나누어 2바이트를 추가한 쉘코드를 사용했다. 
