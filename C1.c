#include <stdio.h>
#include "math.h"

//一个正整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？

int main()
{
	long int i, x, y;
	for (i = 1; i < 100000; i++)
	{
		x = sqrt(i + 100);
		y = sqrt(i + 268);
		if (x * x == i + 100 && y * y == i + 268)
		{
			printf("\n%ld\n", i);
		}
	}
}