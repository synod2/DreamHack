rtld 
-----
#### rtld global overwrite
rtld overwrite는 exit 함수에 의해 프로그램이 종료되는 경우에 사용할 수 있는 기법이다.

exit 함수가 실행 될 때 ```_GI_exit```  -> ```_run_exit_handlers``` -> 
-> ```ld.so/_di_fini``` 순으로 함수들이 연속적으로 호출되는데 , 
이 _dl_fini 함수 하위에서 ```_rtld_lock_lock_recursive(_dl_load_lock)``` 함수가 호출된다. 

```
p _rtld_global

_dl_load_lock = {
mutex = {
  __data = {
    __lock = 0x0, 
    __count = 0x0, 
    __owner = 0x0, 
    __nusers = 0x0, 
    __kind = 0x1, 
    __spins = 0x0, 
    __elision = 0x0, 
    __list = {
      __prev = 0x0, 
      __next = 0x0
    }
  },
  
_dl_rtld_lock_recursive = 0x7ffff7dd60e0 <rtld_lock_default_lock_recursive>, 

gdb-peda$ p &_rtld_global
$3 = (struct rtld_global *) 0x7ffff7ffd060 <_rtld_global>

gdb-peda$ p &_rtld_global._dl_rtld_lock_recursive                                                                 
$7 = (void (**)(void *)) 0x7ffff7ffdf60 <_rtld_global+3840>

gdb-peda$ p &_rtld_global._dl_load_lock
$9 = (__rtld_lock_recursive_t *) 0x7ffff7ffd968 <_rtld_global+2312>


```


_rtld_global 구조체의 멤버인 _rtld_lock_lock_recursive 함수 포인터와 
이 함수의 인자로 사용되는 _dl_load_lock을 덮어써서 원하는 함수를 호출하게 만드는 기법으로, 
두 주소 위치를 각각 덮어씌워 인자와 함수 포인터를 세팅해준다고 생각하면 된다.

_dl_rtld_lock_recursive 와 _dl_load_lock의 주소는 libc base를 기준으로, 
ld base를 찾고 rtld_global 구조체 주소를 찾은 다음 오프셋을 더해줘야 한다. 


---------------------------------------------
```
Ubuntu 16.04
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
```

이 문제는 rtld overwrite를 활용하는 문제다. 프로그램 실행 시 stdout 을 통해 libc 주소를 뿌려주고, 
특정 주소위치에 원하는 값을 입력받게끔 한다. 
본래 해당 기법은 함수 포인터와 인자를 모두 덮어씌워야 하지만, 
지금은 getshell 함수가 있으므로 함수 포인터만 덮으면 될듯. 

PIE가 걸려있는 바이너리라 getshell 함수를 사용하기가 여의치 않아 보이는데 흠..
그냥 원샷가젯을 사용하면 된다. 

라이브러리 버전이 다른경우에는 ld offset도 달라지므로 이에 유의하자.
* 문제에서 별도의 ld 파일을 주지 않아 16버전 우분투로 옮겨서 풀이를 진행하였다. 








