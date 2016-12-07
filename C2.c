#include <stdio.h>

//9*9乘法口诀

int main()
{
	int i, j, res;
	for (i = 1; i < 10; i++) {
		for (j = 1; j < i + 1; j++) {
			res = i * j;
			printf("%d * %d = %-4d", j, i, res);
		}
		printf("\n");
	}
}

