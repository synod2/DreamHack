cpp type confusion
------------------

type confusion ( 자료형 혼동)은 객체나 변수를 선언될 때와 다른 자료형으로 
사용할 때 발생하는 취약점이다. 

이는 주로 C에서 발생하는데 C++은 C에 객체지향 개념을 추가하여 발전된 언어이므로, 
여전히 해당 취약점의 발생 위협이 있다. 

C++에서는 형변환시 dynamic_cast 연산자와 static_cast, reinterpert_cast 연산자를 사용하는데
이중 dynamic_cast연산자만 형변환 과정에서 객체의 형태를 검사하므로, 
나머지 두 연산자는 형변환시 type confusion 취약점이 발생할 수 있다는 것. 

클래스와 같은 객체에서 취약점이 발생 시, 
멤버를 참조할 때 시작 포인터를 기준으로 상대적인 오프셋을 이용해 동작하므로 
원하지 않은 멤버 변수나 함수를 실행시킬 위험이 있다.

```
ex)
print *p1 = new Print();
read *p2 = new Read();

위와 같이 선언되었을 때, 
Print 로 선언된 객체 p1 -> print() 멤버 함수 호출 시,
* p1 + offset = print() 의 형태로 주소값을 계산하여 함수 호출이 이뤄진다.

이때 static_cast 연산자를 활용해 static_cast<print*>(p2) 로 형변환이 이뤄지는 경우, 
원래는 p2 -> read() 처럼 호출할 떄 
*p2 + offset = read() 로 함수 호출이 이뤄져야 하지만 , 
p2 -> print()를 하더라도, 원래 저장된 오프셋 연산에 따라 read() 함수가 호출된다는 것. 

```

이제 문제를 분석해보자. 
apple 과 mango 객체, 클래스는 yum() 멤버 함수를 가진 클래스 Base를 상속해서 만들어진다.
mixer 객체는 Apple 클래스를 상속해서 만들어진다. 

base->yum() 멤버 함수는 base에서는 아무 동작도 하지 않지만,
Apple과 Mango에서는 문자열을 출력하는 동작을 한다. 

1,2 메뉴는 각각 apple과 mango를 선언하고, 
3 메뉴는 mango를 apple로 형변환하여 applemango 에 저장한다. 

apple 클래스는 각각 yum 함수, 생성자, 소멸자, description 변수 순서로 멤버를 가지고 있고 
yum 함수에서 description 문자열을 출력한다.

mango 클래스도 각각 yum 함수, 생성자, 소멸자, description 변수 순서로 멤버를 가지는데
yum 함수에서는 함수 포인터로 선언된 description 을 호출시킨다. 
mango 클래스가 생성될 때는 생성자에 의하여
description 포인터에 문자열을 출력하는 mangohi 함수 포인터가 들어가게 되므로 
정상적인 출력 동작이 수행될 수 있다. 

이후 3번 메뉴에서 ststic_cast에 의해 mango가 apple로 형변환되면
description에 문자열을 입력받는 것이 함수 포인터 형태로 들어가게 되어 
yum을 호출할 때 문제가 된다. 
형변환 되어 들어갔지만 클래스에 들어있는 멤버값 자체는 바뀐것이 없기 때문. 
yum 함수는 여전히 함수 포인터를 가지고 실행된다. 
