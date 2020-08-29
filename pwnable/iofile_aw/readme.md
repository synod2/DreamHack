iofile aw 
----------

file 입출력에서 발생할 수 있는 Arbitarary Write 취약점이다. 
fread 함수에 파일 포인터가 전달될 때, 
파일 포인터의 IO_buf_base와 fileno를 조작할 수 있다면 
fread실행시에 내부적으로 호출되는 IO_SYSREAD 에 의해
IO_buf_base로 전달된 메모리 영역에 쓰기가 가능해지는것.

프로그램을 보자. 각기 read, printf, help, exit 커맨드를 입력할 수 있다. 
커맨드를 입력할 떄 오버플로우는 불가하다. 
printf 명령어를 입력하면 스택에 stdin 의 주소가 저장된다. 

