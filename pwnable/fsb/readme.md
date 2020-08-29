string
------
```
Ubuntu 16.04
Arch:     i386-32-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```
32비트 FSB 문제. 5번째 서식문자부터 입력값 영역에 대응된다. 
FSB에서 %n 서식문자는 "여태까지 출력된 문자열의 수" 를
"서식문자에 대응하는 메모리 위치"에 쓰는 동작을 한다. 

문제에서는 ret가 불가한것처럼 보이는 상황이므로, 
다른함수의 got를 덮어씌우고 인자로 bin/sh 를 전달시키자.  
32비트 시스템이므로 원샷가젯의 사용은 힘들어보이고, libc leak을 위해 별도의 조작이 필요해보인다. 

출력을 위해 사용하는 함수는 warnx 함수이고, 해당 함수에 인자를 전달하는게 쉬워보이므로
해당 함수의 got를 덮어써보겠다. 

%71$x 에서 __libc_start_main+241 주소를 가져올 수 있었다. 
print에서 warnx 의 got를 system으로 덮어씌운 다음, 다시 input에서 /bin/sh를 입력해줘야한다 .

그 후에 다시 출력을 시도하면 warnx("/bin/sh") -> system("/bin/sh") 가 실행된다. 



