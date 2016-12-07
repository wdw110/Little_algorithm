#include <stdio.h>

//求两个数的最大公约数和最小公倍数
//利用递归法求n!阶乘

int fact(int n)
{
	int res;
	if (n == 1) {
		return 1;
	}
	else {
		res = n * fact(n - 1);
		return res;
	}
}

int main()
{
	/*
	int a, b, t, r;
	printf("请输入两个数字：\n");
	scanf("%d %d", &a, &b);
	if (a < b)
	{t = a; a = b; b = t;}
	r = a % b;
	int n = a * b;
	while (r != 0) {
		a = b;
		b = r;
		r = a % b;
	}
	printf("这两个数的最大公约数是：%d，最大公倍数是：%d\n", b, n / b);
	*/
	int n;
	printf("请输入数字\n");
	scanf("%d", &n);
	printf("%d的阶乘为%d", n, fact(n));

	return 0;
}