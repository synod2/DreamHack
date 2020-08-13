basic_rop
---------
```
Ubuntu 16.04
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

32비트 기반 rop 문제. ebp-0x44위치에 0x400 바이트만큼 read함수로 입력을 받는다. 
입력 바이트수에 제한이 없기에 기본적인 ROP를 진행해서 execve를 실행하면 될듯. 

몇몇 레지스터에 사용 가능 가젯이 제한적이어서 시스템 콜을 이용하지는 못할것 같고, 
base leak 후 main으로 돌아가 라이브러리에 있는 함수의 주소를 사용해야 할듯하다. 

write로 libc leak 후 read로 bss 영역에 /bin/sh 입력받고, 
다시 메인으로 돌아가 bss 주소를 인자로 system 함수를 ret에 위치시켜 실행한다. 

오랜만에 풀이한 32비트 ROP라 시간이 좀 걸린듯. 


