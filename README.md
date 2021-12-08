# leetcode-file-gen
Generates a nicely formatted source file for the corresponding LeetCode problem
  
Resulting file includes:
- comment with author, date, problem url, problem number/name, and description
- code snippet provided by LeetCode
  
The program can be easily adapted for different programming languages *TODO*.  
  
https://leetcode.com/problemset/all/
  
### Dependencies  
- Python 3.X  
- bs4 - Beautiful Soup (install with `$ sudo apt-get install python3-bs4`)  
- requests  
- json  
  
### Run  
`$ python3 leetcode-file-gen` **problem_id**  
where **problem_id** can be substituted with the desired problem number.  
  
The provided example: 
`$ python3 leetcode-file-gen 1`  
creates a source file for the [1. Two Sum](https://leetcode.com/problems/two-sum) problem with the file name *0001_two_sum.py*.  
  
`$ python3 leetcode-file-gen --all`  
creates the file *all_problems.txt* listing all available problems with their **problem_id** in `$ pwd`.
