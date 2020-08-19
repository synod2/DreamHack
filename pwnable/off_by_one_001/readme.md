off_by_one_001
--------------

```
Ubuntu 16.04
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

age라는 변수가 1로 초기화되어 선언되어있는데, 

문자열 마지막에 \0 을 추가하는 함수에서 총 20바이트를 입력받고 

비교문에서 age값이 0이면 get_shell 함수를 실행하는 프로그램이다. 

0이 아니면, read함수를 통해 name에 20바이트 입력을 다시 받게 한다. 

age 변수는 스택 메모리상에서 name 바로 다음에 위치하고 있는데, 
read_str 함수는 입력한 문자열 바로 뒤에 \x00을 넣어버린다. 따라서 name을 가득 채우면 그 다음에 있는 age가 0 이 되는것.

쉽게 풀리는 문제다 

