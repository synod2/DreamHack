cpp string 
-----------
```
Ubuntu 16.04 LTS
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
```
cpp에서 C언어처럼 read 함수를 사용하기 위해 쓰는 is.read 함수는 버퍼 마지막에 널바이트를
추가하지 않아 메모리 릭이 발생할 수 있다. 

바이너리를 보면, read , write, show의 세가지 기능을 지원하는데 , 
read에서는 flag파일을 ifstream 으로 읽어와 내용을 flag에 저장하고, 
test 파일을 istream으로 읽어와 readbuffer에 내용을 저장한다. 

이후 write를 진행하면 ostream으로 test에 대해 쓰기를 진행하는데, 
writebuffer에 표준입력으로 입력한 값들이 들어간다. 

readbuffer는 64바이트, flag도 64바이트, writebuffer는 string 자료형으로 선언되어 있다. 

show 는 test에서 읽어온 내용을 그대로 출력한다. 

크게 어려울거 없어 보이는게, test에 64바이트 문자열을 저장한 다음 
파일의 내용을 읽어오게 되면
readbuffer 64바이트를 가득 채우고 writebuffer의 영역까지 침범이 일어나게 될 것. 
그러면 show에서 test파일의 내용인 readbuffer 다음인 writebuffer까지 읽어올것으로 예상된다. 
