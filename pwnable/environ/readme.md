environ 
--------
```
Ubuntu 16.04
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX disabled
PIE:      No PIE (0x400000)
RWX:      Has RWX segments
```
코드를 보자 .  프로그램 실행시 stdout, 표준 출력 포인터의 주소값을 출력하고 
scanf 함수를 통해 입력 버퍼의 길이를 정한다. 

그 다음, 정한 길이만큼 문자열을 입력하고 점프할 위치를 입력받는다 . 

이 문제에서 사용하는 취약점은 envrion ptr로, libc에서 환경변수를 참조할 때 사용하는 변수인 
environ안에 스택 주소가 들어가는 점을 이용하는 취약점이다.

evniron은 stdout과 동일하게 libc 영역에 위치하는 변수로,
stdout 오프셋을 통해 environ 주소를 알아내어 사용하는 식으로 풀이를 유도하는것 같다. 
이렇게 알아낸 environ 안에는 스택 주소가 들어있으므로 , 스택에 쉘코드를 넣을 경우 쉘코드 실행까지 가능하다. 

18.04 libc 기준으로 stdout + 0x1938 = environ의 주소였다. 
environ 에 있는 주소는 현재 입력버퍼가 들어가는 스택 + 0x118 위치이므로, 
스택에 0x118 이상 바이트를 넣어주면 입력값에 대해 실행이 가능할것도 같다. 
