basic ex 001
------------

```
Ubuntu 16.04
Arch:     i386-32-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

system("cat flag") 명령어를 실행하는 함수가 바이너리 안에 들어있다. 

버퍼 스택의 크기는 이전 문제와 동일한 0x80이고 nx가 켜져있으니 스택에서의 쉘코드의 사용은 불가하다.

ret 위치에 해당 함수 주소값만 넣어주면 끝. 