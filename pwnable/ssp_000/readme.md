ssp_000
-------
```
Ubuntu 16.04
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```
카나리 보호기법이 활성화된 바이너리. getshell 함수가 있다.

read함수로 0x80 바이트를 입력받아 rbp-0x50에 저장하고, 
rbp-0x60위치에 주소값을 하나 입력받은 다음 , 0x58위치에 또 숫자를 입력받는다. 

이후 연산에서 rbp-0x60이 가리키는 주소 위치에 rbp-0x58에 있는 값을 집어넣게 된다. 

카나리가 활성화되어있기 때문에 정해진 스택 크기를 넘어가 카나리 변조가 일어나면 
__stack_chk_fail 함수가 실행된다.

원하는 위치에 원하는 값을 입력할 수 있으므로 해당 함수의 got를 쉘 함수로 변조하고, 
고의로 카나리 변조를 발생시켜보자. 
