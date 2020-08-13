sint
----
```
Ubuntu 16.04
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

scanf로 숫자를 입력받고 입력받은 숫자가 0x100 보다 크다면 buffer overflow라는 문자열을 띄우고 종료를,
그렇지 않다면 read함수에서 입력한 숫자-1 만큼 입력을 받게 한다 . 
그리고, 입력한 숫자가 음수인 경우도 마찬가지로 처리한다. 

문자열을 입력받는 스택 위치는 ebp-0x100 위치이므로 , 일반적인 방법으로는 오버플로우가 어려워 보이는 상황.
그러나 입력한 숫자가 0인 경우에 대한 처리 구문이 없고, 0을 입력한 경우엔 read 함수에서 문자열 길이 인자가 -1인 상태로 입력을 받게된다. 
이경우에는 0xffffffff 만큼 입력을 받게 되므로, 오버플로우가 가능해진다.



