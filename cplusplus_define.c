#include<stdio.h>
#define a 1+1
#define b 1+1
int main(){
	if(a!=b){
		printf("lose\n");
		return 0;
	}else if(a-b==0){
		printf("lose\n");
		return 0;
	}
	printf("win!\n");
	return 0;
}
/*

output:

win!

*/
