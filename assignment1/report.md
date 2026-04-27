---
layout: page
title: Assignment 1 Report
---

# Remote Development Project Report



\*\*Student Name\*\*: WuYuekai  

\*\*Student ID\*\*: ZY2557209



\## System Configuration



This project was completed on Windows using Git Bash. Some Linux-specific commands such as `lscpu` and `free -h` were not available in this environment, so PowerShell commands were used to collect CPU, memory, and operating system information.



| Item | Command | Result |

|---|---|---|

| CPU Model | `powershell -Command "Get-CimInstance Win32\_Processor \\| Select-Object -ExpandProperty Name"` | Intel(R) Core(TM) i7-14700HX |

| Memory Size | `powershell -Command "\[math]::Round((Get-CimInstance Win32\_ComputerSystem).TotalPhysicalMemory / 1GB, 2)"` | 31.78 GB |

| Operating System | `powershell -Command "Get-CimInstance Win32\_OperatingSystem \\| Select-Object -ExpandProperty Caption"` | Microsoft Windows 11 家庭中文版 |

| OS Version | `cmd /c ver` | Microsoft Windows \[版本 10.0.26200.8246] |

| Git Bash System Info | `uname -a` | MINGW64\_NT-10.0-26200 kk 3.6.6-1cdd4371.x86\_64 2026-01-15 22:20 UTC x86\_64 Msys |

| Compiler Version | `gcc --version` | GCC not installed |

| Python Version | `python --version` | Python 3.12.10 |



\## Implementation Details



The main task of this project is to implement matrix multiplication using an interpreted language. I used Python because it is easy to read, simple to run, and suitable for demonstrating basic algorithms.



Matrix multiplication takes two matrices A and B. If A has size m × n and B has size n × p, the result matrix C has size m × p. Each element of C is calculated by multiplying one row from A with one column from B and summing the products.



\## Python Language Implementation



\### Source Code



The Python source code is shown below.



```python

\# matrix\_multiply.py

\# This program demonstrates matrix multiplication using Python.



def matrix\_multiply(A, B):

&#x20;   """

&#x20;   Multiply two matrices A and B.



&#x20;   A is an m x n matrix.

&#x20;   B is an n x p matrix.

&#x20;   The result C is an m x p matrix.

&#x20;   """



&#x20;   rows\_A = len(A)

&#x20;   cols\_A = len(A\[0])

&#x20;   rows\_B = len(B)

&#x20;   cols\_B = len(B\[0])



&#x20;   # Check whether the two matrices can be multiplied

&#x20;   if cols\_A != rows\_B:

&#x20;       raise ValueError("Matrix dimensions do not match for multiplication.")



&#x20;   # Create a result matrix filled with zeros

&#x20;   C = \[\[0 for \_ in range(cols\_B)] for \_ in range(rows\_A)]



&#x20;   # Matrix multiplication:

&#x20;   # C\[i]\[j] = sum(A\[i]\[k] \* B\[k]\[j])

&#x20;   for i in range(rows\_A):

&#x20;       for j in range(cols\_B):

&#x20;           for k in range(cols\_A):

&#x20;               C\[i]\[j] += A\[i]\[k] \* B\[k]\[j]



&#x20;   return C





def print\_matrix(M):

&#x20;   """Print a matrix row by row."""

&#x20;   for row in M:

&#x20;       print(row)





if \_\_name\_\_ == "\_\_main\_\_":

&#x20;   # Test matrices

&#x20;   A = \[

&#x20;       \[1, 2],

&#x20;       \[3, 4]

&#x20;   ]



&#x20;   B = \[

&#x20;       \[5, 6],

&#x20;       \[7, 8]

&#x20;   ]



&#x20;   print("Matrix A:")

&#x20;   print\_matrix(A)



&#x20;   print("\\nMatrix B:")

&#x20;   print\_matrix(B)



&#x20;   C = matrix\_multiply(A, B)



&#x20;   print("\\nResult of A x B:")

&#x20;   print\_matrix(C)



&#x20;   print("\\nExpected result:")

&#x20;   print("\[19, 22]")

&#x20;   print("\[43, 50]")

The Python script can be executed with the following command:

python matrix\_multiply.py

The output is:



Matrix A:

\[1, 2]

\[3, 4]



Matrix B:

\[5, 6]

\[7, 8]



Result of A x B:

\[19, 22]

\[43, 50]



Expected result:

\[19, 22]

\[43, 50]

Algorithm Verification



To verify the correctness of the matrix multiplication algorithm, I used a small 2 × 2 matrix example that can be calculated manually.



The test matrices are:



A = \[\[1, 2],

&#x20;    \[3, 4]]



B = \[\[5, 6],

&#x20;    \[7, 8]]



The expected result is:



C = \[\[19, 22],

&#x20;    \[43, 50]]



Manual calculation:



C\[0]\[0] = 1 × 5 + 2 × 7 = 19

C\[0]\[1] = 1 × 6 + 2 × 8 = 22

C\[1]\[0] = 3 × 5 + 4 × 7 = 43

C\[1]\[1] = 3 × 6 + 4 × 8 = 50



The program output matches the manually calculated result. Therefore, the implementation is correct for this test case.



C Language Implementation and Performance Analysis (bonus)



I did not complete the optional C language implementation because GCC was not installed in my current environment. The required command gcc --version returned command not found.



Conclusion



In this assignment, I practiced using command line tools, writing Markdown documentation, and implementing a basic matrix multiplication algorithm in Python. I also learned how to collect system information from the command line. Since my environment was Windows with Git Bash, I used PowerShell commands to collect some system information that would normally be collected using Linux commands.



Through the Python implementation, I learned how matrix multiplication works using three nested loops. I also verified the correctness of the algorithm by comparing the program output with a manually calculated result.



References

Python documentation: https://docs.python.org/3/

Git documentation: https://git-scm.com/doc

Markdown Guide: https://www.markdownguide.org/

Microsoft PowerShell documentation: https://learn.microsoft.com/en-us/powershell/

Appendix

Additional Notes



This project was completed in a Windows environment using Git Bash. Some Linux-specific commands were unavailable, so equivalent PowerShell commands were used when necessary.

