io file vtable check
--------------------
```
Ubuntu 18.04
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

소스를 보면, 파일을 열고 fp에 저장한 다음, read 함수로 fp 위치에 300바이트만큼 
입력을 받고 있다. 