#include <stdlib.h>
#include <stdio.h>

#define dprint(expr) printf(#expr " = %g\n",expr)
#define paste(front,back) front ## back
#define swap(t,x,y) {int tmp=t.x;t.x=t.y;t.y=tmp;}
#define val1 1+1
#define val2 1+1

struct AA{
	int a,b,c;
};
struct AA test;
int main(){
	//dprint
	float x=3,y=4;
	dprint(x/y);

	//paste
	int n1=0,n2=0,n3=0;
	paste(n,1)=666;
	paste(n,2)=777;
	paste(n,3)=888;
	printf("v :%d\n",n1);
	printf("v :%d\n",n2);
	printf("v :%d\n",n3);

	//swap
	test.a=1;
	test.b=2;
	test.c=3;
	swap(test,a,b);
	swap(test,b,c);
	printf("v :%d\n",test.a);
	printf("v :%d\n",test.b);
	printf("v :%d\n",test.c);

	if(val1!=val2){
		printf("lose\n");
		return 0;
	}else if(val1-val2==0){
		printf("lose\n");
		return 0;
	}
	printf("win!\n");
	
	return 0;
}

/*
Output:

x/y = 0.75
v :666
v :777
v :888
v :2
v :3
v :1
win!

*/
