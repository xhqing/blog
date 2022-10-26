创建于 2022-09-26
关键词: taichi, Python, compute-intensive, parallel.

## What is Taichi

Taichi github repo: https://github.com/taichi-dev/taichi 

Official docs: https://www.taichi-lang.org/

Taichi Lang is an open-source, imperative, parallel programming language for high-performance numerical computation. It is embedded in Python and uses just-in-time (JIT) compiler frameworks, for example LLVM, to offload the compute-intensive Python code to the native GPU or CPU instructions.

![fractal_small](img/fractal_small.gif)

## Primes Count 

```sh
vim count_primes_without_taichi.py
```

```python
"""Count the number of primes in range [1, n].
"""
import time

def is_prime(n: int):
    result = True
    for k in range(2, int(n**0.5)+1):
        if n % k == 0: 
            result = False
            break
    return result

def count_primes(n: int) -> int:
    count = 0
    for k in range(2, n):
        if is_prime(k): 
            count += 1
    return count

start_time = time.time()
print(count_primes(1000000))
end_time = time.time()
print("time cost: {}s".format(end_time-start_time))
```

```sh
python count_primes_without_taichi.py

78498
time cost: 3.318950891494751s
```

```sh
vim count_primes_with_taichi.py
```

```python
"""Count the number of primes in range [1, n].
"""
import time
import taichi as ti
ti.init()

@ti.func
def is_prime(n: int):
    result = True
    for k in range(2, int(n**0.5)+1):
        if n % k == 0: 
            result = False
            break
    return result

@ti.kernel
def count_primes(n: int) -> int:
    count = 0
    for k in range(2, n):
        if is_prime(k): 
            count += 1
    return count

start_time = time.time()
print(count_primes(1000000))
end_time = time.time()
print("time cost: {}s".format(end_time-start_time))
```

```sh
python count_primes_with_taichi.py

[Taichi] version 1.1.3, llvm 10.0.0, commit 1262a70a, osx, python 3.9.12
[Taichi] Starting on arch=arm64
78498
time cost: 0.08886313438415527s
```

## Longest Commom Sequence

```sh
vim lcs_without_taichi.py
```

```python
"""Longest Common Sequence
"""
import numpy as np
import time


benchmark = True

N = 15000

f = np.zeros(shape=(N+1, N+1), dtype=np.int32)

if benchmark:
    a_numpy = np.random.randint(0, 100, N, dtype=np.int32)
    b_numpy = np.random.randint(0, 100, N, dtype=np.int32)
else:
    a_numpy = np.array([0,1,0,2,4,3,1,2,1], dtype=np.int32)
    b_numpy = np.array([4,0,1,4,5,3,1,2], dtype=np.int32)

def compute_lcs(a, b):
    len_a, len_b = a.shape[0], b.shape[0]

    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            f[i, j] = max(f[i-1, j-1] + (a[i-1] == b[j-1]), max(f[i-1, j], f[i, j-1]))

    return f[len_a, len_b]

start_time = time.time()
print(compute_lcs(a_numpy, b_numpy))
end_time = time.time()
print("time cost: {}s".format(end_time-start_time))
```

```sh
python lcs_without_taichi.py

2687
time cost: 229.79690885543823s
```

```sh
vim lcs_with_taichi.py
```

```python
"""Longest Common Sequence
"""
import taichi as ti
import numpy as np
import time

ti.init(arch=ti.cpu)

benchmark = True

N = 15000

f = ti.field(dtype=ti.i32, shape=(N + 1, N + 1))

if benchmark:
    a_numpy = np.random.randint(0, 100, N, dtype=np.int32)
    b_numpy = np.random.randint(0, 100, N, dtype=np.int32)
else:
    a_numpy = np.array([0,1,0,2,4,3,1,2,1], dtype=np.int32)
    b_numpy = np.array([4,0,1,4,5,3,1,2], dtype=np.int32)

@ti.kernel
def compute_lcs(a: ti.types.ndarray(), b: ti.types.ndarray()) -> ti.i32:
    len_a, len_b = a.shape[0], b.shape[0]

    ti.loop_config(serialize=True)
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            f[i, j] = max(f[i-1, j-1] + (a[i-1] == b[j-1]), max(f[i-1, j], f[i, j-1]))

    return f[len_a, len_b]

start_time = time.time()
print(compute_lcs(a_numpy, b_numpy))
end_time = time.time()
print("time cost: {}s".format(end_time-start_time))
```

```sh
python lcs_with_taichi.py

[Taichi] version 1.1.3, llvm 10.0.0, commit 1262a70a, osx, python 3.9.12
[Taichi] Starting on arch=arm64
2701
time cost: 1.5659801959991455s
```



