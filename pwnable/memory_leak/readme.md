memory_leak
-----------
```
Ubuntu 16.04
Arch:     i386-32-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```
3개의 메뉴가 나오고, 1은 정보 입력 2는 정보 출력 3은 fopen으로 플래그 읽어와 flag_buf에 저장한다. 
일단 메모리상에 어떻게 저장되는지부터 확인을 해보면, my_page 구조체의 name, age 다음에 바로 플래그를 저장한다. 
이렇게 하면 2번 메뉴 출력시에 모든 메모리 영역을 꽉 채울 경우 연속적인 참조가 가능할것도 같다. 

이름 입력시엔 16바이트 전체르 다 채우고, 나이 입력시엔 음수를 입력해 해당 메모리가 0xfffffff 로 꽉차게 하자. 

