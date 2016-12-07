#include <stdio.h>

//对10个数排序

#define N 10

int main()
{
	int i, j, a[N], temp;
	printf("请输入10个数字：\n");
	for (i = 0; i < N; i++) {
		scanf("%d", &a[i]);
	}
	for (i = 0; i < N; i++) {
		int min = i;
		for (j = i + 1; j < N; j++)
			if (a[min] > a[j]) min = j;
		if (min != i) {
			temp = a[min];
			a[min] = a[i];
			a[i] = temp;
		}
	}
	printf("排序结果是：\n");
	for (i = 0; i < N; i++)
		printf("%d*", a[i]);
	printf("\n");

	return 0;
}