vtable 
-------

```
Ubuntu 16.04
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

vtable 관련 취약점은 18.04 이후에선 다르게 동작하기 때문에 
문제와 동일한 환경인 16.04에서 풀이를 진행한다. 

프로그램 시작시 전역변수 영역에 8바이트 입력을 받고, 메뉴를 고를 수 있는데 

1번은 good을 출력, 
2번은 fprintf를 실행하고 stderr 에 ERROR를 쓰는 작업, 
3번은 fgetc로 입력을 받고
4번은 stderr+1 위치에 8바이트 입력을 받는다. 
디버깅을 통해 좀 더 자세히 보자. 

4번에서 stderr+1 위치는 구조체 크기에 따라 실제로는 stderr + 0xd8 주소 위치를 가리키게 된다. 
이때 문자열을 입력해준 상태로 2번 메뉴 실행시 에러가 발생하면서 프로그램이 종료된다 .

* 18.04 버전기준 ("Fatal error: glibc detected an invalid stdio handle\n") 에러 발생 

이는 stderr의 vtable 포인터가 변조되었기 때문. 

파일 입출력 시에 각 FP 는 파일 스트림 구조체를 구성하면서 vtable을 가리키는 포인터를 가지고, 
vtable 구조체 안에는 여러가지 멤버 함수들의 포인터들이 들어간다. 

FSOP 공격을 위해선 원하는 함수 주소가 들어가는 가짜 Vtable을 구성하고, 
해당 파일 스트림의 vtable 포인터가 들어있는 위치의 값을 변조하여 
가짜 vtable을 가리키게 만들어야 한다. 

그렇게 되면 이후에 트리거 발생 시 해당 트리거에 의해 호출되는 변조된 함수가 실행된다.
(ex - fclose 함수가 실행될 경우 해당 파일 스트림에서 IO_FINISH 함수가 실행되는데, 
이 함수는 파일 스트림이 가지고 있는 vtable 구조체의 멤버로 존재한다. )

stdin, stderr, stderr는 프로세스가 시작 될 때 라이브러리에 의해 자동으로 생성되는 파일 스트림으로,
이 또한 일반적인 파일 스트림과 동일하게 vtable을 가지고 파일 입출력 동작에 동일하게 반응한다.

파일 포인터에서 주로 트리거되는 함수는 fclose시의 ```IO_FINISH(+0x10)```, 
fread시의 ```IO_sgetn(+0x40)``` 등이 있는데, 
이 문제에서는 fprintf, 내부적으로는 fwrite 함수를 이용해 트리거를 유도하기에 ```IO_sputn(+0x38)``` 을 호출시켜야 한다. 
즉, vtable + 0x38 위치에 원하는 함수의 주소를 삽입하면 될거란 얘기. 

```
gdb-peda$ x/x $rbp
0x7ffff7dd2540 <_IO_2_1_stderr_>:       0x00000000fbad2086

			   <+203>:   mov    rax,QWORD PTR [rbp+0xd8]
			   <+210>:   mov    rdx,rbx
			   <+213>:   mov    rdi,rbp
<__GI__IO_fwrite+216>:        call   QWORD PTR [rax+0x38]
```
디버거로 좀 더 자세히 들여다보면, rbp가 stderr 주소를 가리키는 상황에서, 
rbp+0xd8 위치에 있는 값을 (vtable 포인터) rax 레지스터로 가져오고,
rax+0x38 에 있는 주소 (IO_sputn 함수 포인터)에 call을 수행하는 걸 볼 수 있다. 

IO_sputn이라는 걸 몰라도, 파일 스트림 관련 함수가 호출되는 내부를 잘 뜯어보면 
어떤 위치에 대해 vtable 조작을 시행해야 할 지를 알 수 있단 소리. 

stderr의 vtable을 조작할 수 있고, 전역변수 영역에 입력을 받을 수 있는데다가 
전역변수 주소값도 알수있다. 전역변수 주소-0x38 을 vtable에 넣어주고, 
전역변수 주소에는 쉘 함수를 실행시킬 수 있는 주소를 박아주자.  





