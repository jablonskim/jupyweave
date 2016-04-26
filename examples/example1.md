Markdown example
================
<!!![Python 3] timeout=5000>
Testtesttest
------------

1. Test test

Te*s*t

<#[Python 3] echo=T output=T>
for i in range(10):
    print(i)

print('Test')
<@>

T**es**t

> qqq

> qqq

Link [example](https://pl.wikipedia.org/wiki/Markdown)

<#>
%matplotlib inline
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2

x = np.linspace(0, 3*np.pi, 500)
plt.plot(x, np.sin(f(x)))
plt.title('A simple chirp')
print('before')
plt.show()
print('after')
<@>

Test `Test` Test

