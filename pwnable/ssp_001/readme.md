ssp_001 
--------

```
Ubuntu 16.04
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

카나리가 걸려있는 문제. getshell 함수가 있으므로 카나리를 잘 우회하여 쉘을 넣어보자. 
F로 박스에 입력, P로 특정 메모리 위치 출력, E 입력시 이름 길이와 이름을 입력받고 프로그램을 종료한다. 

이름 입력 크기 제한이 따로 없다. P에서 카나리를 전부 뽑아낸 다음 E에서 오버플로우를 진행해보자. 
P에서 0x80 부터 카나리 위치에 접근이 가능해보인다. 83 82 81 80 순으로 뽑아내면 카나리 전체가 완성된다.

이름 입력시 0x40 + 카나리 + dummy4 + ebp + ret 까지 하면 ret를 덮을수 있을 듯. 




