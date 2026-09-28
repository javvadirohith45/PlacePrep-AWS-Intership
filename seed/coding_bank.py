"""Generated-but-curated starter coding bank. 210 distinct placement-oriented problems."""

from models.content import CodingLanguage, CodingProblem, CodingTestCase
from extensions import db


def _io_case(lang, idx):
    # Deterministic, language-neutral test payloads.
    cases = [
        ("5\n2 4 6 8 10\n", "30"),
        ("6\n3 8 2 9 4 7\n", "9"),
        ("6\n5 1 5 2 5 3\n5\n", "3"),
        ("7\n1 2 3 4 5 6 7\n3\n", "4 5 6 7 1 2 3"),
        ("racecar\n", "YES"),
        ("placement prep\n", "9"),
        ("10 15\n", "5"),
        ("12\n", "144"),
        ("8\n", "21"),
        ("6\n", "720"),
        ("10\n", "55"),
        ("29\n", "PRIME"),
        ("12 18\n", "6"),
        ("12 18\n", "36"),
        ("1 2 2 3 3 4\n", "1 2 3 4"),
        ("7\n4 1 9 2 7 3 8\n", "1 2 3 4 7 8 9"),
        ("7\n4 1 9 2 7 3 8\n7\n", "4"),
        ("4\n1 2 3 4\n", "1 3 6 10"),
        ("3 3\n1 2 3\n4 5 6\n7 8 9\n", "15"),
        ("5\n2 3 4 5 6\n", "120"),
        ("hello world\n", "world hello"),
        ("aabbccdde\n", "e"),
        ("6\n10 20 10 30 20 40\n", "10 20 30 40"),
        ("5\n1 1 2 2 3\n", "3"),
        ("4\n5 10 15 20\n", "50"),
        ("5\n10 20 30 40 50\n", "30"),
        ("7\n1 2 3 4 5 6 7\n", "28"),
        ("5\n8 6 7 5 3\n", "3 5 6 7 8"),
        ("4\n2 4 6 8\n", "4"),
        ("5\n1 2 3 4 5\n2\n", "1 3 5"),
        ("4\n1 2 3 4\n", "24"),
        ("6\n1 1 1 2 2 3\n", "1:3 2:2 3:1"),
        ("4\n10 20 30 40\n", "40 30 20 10"),
        ("5\n2 7 11 15 20\n", "11"),
        ("6\n3 5 8 13 21 34\n", "84"),
        ("3 4\n", "12"),
        ("5\n9 7 5 3 1\n", "1"),
    ]

    return cases[idx % len(cases)]


def _starter(lang, recipe):
    """Return starter code for non-SQL languages."""

    py = [
        '''import sys

def main():
    data = sys.stdin.read().strip().split()

    # TODO: implement the problem
    print("0")

if __name__ == "__main__":
    main()
''',

        '''import sys
from collections import Counter

def main():
    s = sys.stdin.read().strip()

    # TODO: implement using Python collections
    print(len(s))

if __name__ == "__main__":
    main()
''',

        '''import sys

def main():
    data = list(map(int, sys.stdin.read().split()))

    # TODO: implement the requested transformation
    print(*data)

if __name__ == "__main__":
    main()
'''
    ]

    if lang == "python":
        return py[recipe % len(py)]

    if lang == "javascript":
        return '''const fs = require('fs');

const data = fs.readFileSync(0, 'utf8').trim().split(/\\s+/);

// TODO: implement the problem using modern JavaScript
console.log(data.length ? data.length : 0);
'''

    if lang == "java":
        return '''import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);

        // TODO: implement the problem using Java collections/algorithms
        System.out.println(0);
    }
}
'''

    if lang == "cpp":
        return '''#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // TODO: implement the problem using STL
    cout << 0 << '\\n';

    return 0;
}
'''

    if lang == "c":
        return '''#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void) {

    /* TODO: implement the problem using C arrays/pointers/functions */
    printf("0\\n");

    return 0;
}
'''

    return ""


# ---------------------------------------------------------------------------
# SQL FIXTURE
# ---------------------------------------------------------------------------

SQL_FIXTURE = """CREATE TABLE employees(
    id INTEGER,
    name TEXT,
    department TEXT,
    salary INTEGER,
    manager_id INTEGER
);

INSERT INTO employees VALUES
(1,'Asha','Engineering',90000,NULL),
(2,'Ravi','Engineering',70000,1),
(3,'Mina','HR',60000,NULL),
(4,'Kiran','HR',65000,3),
(5,'Dev','Sales',55000,NULL),
(6,'Sara','Sales',80000,5),
(7,'Ira','Engineering',95000,1);

CREATE TABLE customers(
    id INTEGER,
    name TEXT
);

INSERT INTO customers VALUES
(1,'Asha'),
(2,'Ravi'),
(3,'Mina'),
(4,'Dev');

CREATE TABLE orders(
    id INTEGER,
    customer_id INTEGER,
    amount INTEGER,
    order_date TEXT,
    status TEXT
);

INSERT INTO orders VALUES
(101,1,120,'2026-01-02','paid'),
(102,1,80,'2026-01-08','paid'),
(103,2,200,'2026-01-09','paid'),
(104,3,50,'2026-01-10','cancelled'),
(105,3,75,'2026-02-01','paid'),
(106,4,300,'2026-02-04','paid');

CREATE TABLE tickets(
    id INTEGER,
    customer_id INTEGER,
    status TEXT,
    updated_at TEXT
);

INSERT INTO tickets VALUES
(1,1,'open','2026-02-01'),
(2,1,'closed','2026-02-03'),
(3,2,'open','2026-02-02'),
(4,3,'pending','2026-02-04');

CREATE TABLE products(
    id INTEGER,
    name TEXT,
    price INTEGER
);

INSERT INTO products VALUES
(1,'Keyboard',50),
(2,'Mouse',25),
(3,'Monitor',200),
(4,'Stand',75);

CREATE TABLE sales(
    product_id INTEGER,
    qty INTEGER
);

INSERT INTO sales VALUES
(1,3),
(2,5),
(3,2),
(4,1);

CREATE TABLE email_records(
    id INTEGER,
    email TEXT
);

INSERT INTO email_records VALUES
(1,'asha@example.com'),
(2,'ravi@example.com'),
(3,'asha@example.com'),
(4,'mina@example.com'),
(5,'ravi@example.com'),
(6,'dev@example.com');

CREATE TABLE user_logins(
    user_id INTEGER,
    login_date TEXT
);

INSERT INTO user_logins VALUES
(1,'2026-02-01'),
(1,'2026-02-02'),
(1,'2026-02-03'),
(1,'2026-02-05'),
(2,'2026-02-01'),
(2,'2026-02-03'),
(2,'2026-02-04'),
(2,'2026-02-05'),
(3,'2026-02-10'),
(3,'2026-02-11'),
(3,'2026-02-12');
"""


# ---------------------------------------------------------------------------
# SQL QUESTIONS
# ---------------------------------------------------------------------------

SQL_TASKS = [
    (
        "Department Salary Totals",
        "SELECT department, SUM(salary) AS total_salary "
        "FROM employees GROUP BY department ORDER BY department;",
        "Engineering|255000\\nHR|125000\\nSales|135000"
    ),
    (
        "Employees Above Department Average",
        "SELECT name FROM employees e "
        "WHERE salary > (SELECT AVG(salary) FROM employees x "
        "WHERE x.department=e.department) ORDER BY name;",
        "Asha\\nIra\\nKiran\\nSara"
    ),
    (
        "Second Highest Salary",
        "SELECT MAX(salary) FROM employees "
        "WHERE salary < (SELECT MAX(salary) FROM employees);",
        "90000"
    ),
    (
        "Duplicate Email Detector",
        "SELECT email FROM email_records "
        "GROUP BY email HAVING COUNT(*) > 1 ORDER BY email;",
        "asha@example.com\\nravi@example.com"
    ),
    (
        "Monthly Revenue Summary",
        "SELECT substr(order_date,1,7), SUM(amount) "
        "FROM orders WHERE status='paid' "
        "GROUP BY substr(order_date,1,7) ORDER BY 1;",
        "2026-01|400\\n2026-02|375"
    ),
    (
        "Customers Without Orders",
        "SELECT c.name FROM customers c "
        "LEFT JOIN orders o ON o.customer_id=c.id "
        "WHERE o.id IS NULL ORDER BY c.name;",
        ""
    ),
    (
        "Employees With Managers",
        "SELECT e.name, m.name FROM employees e "
        "JOIN employees m ON e.manager_id=m.id ORDER BY e.name;",
        "Ira|Asha\\nKiran|Mina\\nRavi|Asha\\nSara|Dev"
    ),
    (
        "Top Earner Per Department",
        "SELECT department,name FROM ("
        "SELECT department,name,salary,"
        "ROW_NUMBER() OVER(PARTITION BY department ORDER BY salary DESC) rn "
        "FROM employees) WHERE rn=1 ORDER BY department;",
        "Engineering|Ira\\nHR|Kiran\\nSales|Sara"
    ),
    (
        "Running Revenue Total",
        "SELECT id, SUM(amount) OVER(ORDER BY id) "
        "FROM orders WHERE status='paid' ORDER BY id;",
        "101|120\\n102|200\\n103|400\\n105|475\\n106|775"
    ),
    (
        "Rank Products By Sales",
        "SELECT p.name, p.price*s.qty AS revenue, "
        "RANK() OVER(ORDER BY p.price*s.qty DESC) "
        "FROM products p JOIN sales s ON s.product_id=p.id "
        "ORDER BY 2 DESC;",
        "Monitor|400|1\\nKeyboard|150|2\\nMouse|125|3\\nStand|75|4"
    ),
    (
        "Consecutive Login Days",
        "WITH numbered AS ("
        "SELECT user_id, login_date, "
        "date(login_date, '-' || "
        "ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_date) || ' days') AS grp "
        "FROM user_logins) "
        "SELECT user_id, COUNT(*) AS consecutive_days "
        "FROM numbered GROUP BY user_id, grp "
        "HAVING COUNT(*) >= 3 ORDER BY user_id, consecutive_days DESC;",
        "1|3\\n2|3\\n3|3"
    ),
    (
        "First Order Per Customer",
        "SELECT customer_id, MIN(order_date) "
        "FROM orders WHERE status='paid' "
        "GROUP BY customer_id ORDER BY customer_id;",
        "1|2026-01-02\\n2|2026-01-09\\n3|2026-02-01\\n4|2026-02-04"
    ),
    (
        "Latest Status Per Ticket",
        "SELECT id,status FROM tickets "
        "ORDER BY updated_at DESC;",
        "4|pending\\n2|closed\\n3|open\\n1|open"
    ),
    (
        "Average Salary By Role",
        "SELECT department, ROUND(AVG(salary),2) "
        "FROM employees GROUP BY department ORDER BY department;",
        "Engineering|85000.0\\nHR|62500.0\\nSales|67500.0"
    ),
    (
        "Conditional Salary Bands",
        "SELECT name, CASE "
        "WHEN salary>=90000 THEN 'High' "
        "WHEN salary>=65000 THEN 'Mid' "
        "ELSE 'Entry' END "
        "FROM employees ORDER BY id;",
        "Asha|High\\nRavi|Mid\\nMina|Entry\\nKiran|Mid\\n"
        "Dev|Entry\\nSara|Mid\\nIra|High"
    ),
    (
        "Null Safe Department Label",
        "SELECT name, COALESCE(department,'Unassigned') "
        "FROM employees WHERE manager_id IS NULL ORDER BY id;",
        "Asha|Engineering\\nMina|HR\\nDev|Sales"
    ),
    (
        "Join Three Business Tables",
        "SELECT c.name, SUM(o.amount) "
        "FROM customers c JOIN orders o "
        "ON o.customer_id=c.id "
        "WHERE o.status='paid' "
        "GROUP BY c.id,c.name ORDER BY c.id;",
        "Asha|200\\nRavi|200\\nMina|75\\nDev|300"
    ),
    (
        "Products Never Sold",
        "SELECT p.name FROM products p "
        "LEFT JOIN sales s ON s.product_id=p.id "
        "WHERE s.product_id IS NULL ORDER BY p.name;",
        ""
    ),
    (
        "Orders Above Customer Average",
        "SELECT o.id FROM orders o "
        "WHERE o.amount > ("
        "SELECT AVG(x.amount) FROM orders x "
        "WHERE x.customer_id=o.customer_id) "
        "ORDER BY o.id;",
        "101\\n105"
    ),
    (
        "Duplicate Transaction Groups",
        "SELECT customer_id, COUNT(*) "
        "FROM orders GROUP BY customer_id "
        "HAVING COUNT(*)>1 ORDER BY customer_id;",
        "1|2\\n3|2"
    ),
    (
        "Seven Day Rolling Average",
        "SELECT id, ROUND("
        "AVG(amount) OVER("
        "ORDER BY order_date "
        "ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) "
        "FROM orders WHERE status='paid' ORDER BY id;",
        "101|120.0\\n102|100.0\\n103|133.33\\n105|118.33\\n106|191.67"
    ),
    (
        "Percent Of Department Total",
        "SELECT name, ROUND("
        "100.0*salary/SUM(salary) OVER(PARTITION BY department),2) "
        "FROM employees ORDER BY id;",
        "Asha|35.29\\nRavi|27.45\\nMina|48.0\\nKiran|52.0\\n"
        "Dev|40.74\\nSara|59.26\\nIra|37.25"
    ),
    (
        "Customers With Multiple Orders",
        "SELECT customer_id FROM orders "
        "GROUP BY customer_id HAVING COUNT(*)>1 "
        "ORDER BY customer_id;",
        "1\\n3"
    ),
    (
        "Pivot Status Counts",
        "SELECT status, COUNT(*) FROM orders "
        "GROUP BY status ORDER BY status;",
        "cancelled|1\\npaid|5"
    ),
    (
        "Median Salary By Department",
        "SELECT department, AVG(salary) FROM ("
        "SELECT department,salary,"
        "ROW_NUMBER() OVER(PARTITION BY department ORDER BY salary) rn,"
        "COUNT(*) OVER(PARTITION BY department) cnt "
        "FROM employees) "
        "WHERE rn IN ((cnt+1)/2,(cnt+2)/2) "
        "GROUP BY department ORDER BY department;",
        "Engineering|90000.0\\nHR|62500.0\\nSales|67500.0"
    ),
    ('Departments With More Than One Employee', 'SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 1 ORDER BY department;', 'Engineering|3\nHR|2\nSales|2'),
    ('Paid Revenue By Customer', "SELECT c.name, COALESCE(SUM(CASE WHEN o.status='paid' THEN o.amount ELSE 0 END),0) FROM customers c LEFT JOIN orders o ON o.customer_id=c.id GROUP BY c.id,c.name ORDER BY c.name;", 'Asha|200\nDev|300\nMina|75\nRavi|200'),
    ('Largest Order', 'SELECT MAX(amount) FROM orders;', '300'),
    ('Customers With Open Tickets', "SELECT c.name FROM customers c JOIN tickets t ON t.customer_id=c.id WHERE t.status='open' ORDER BY c.name;", 'Asha\\nRavi'),
    ('Product Sales Revenue', 'SELECT p.name, COALESCE(SUM(p.price*s.qty),0) FROM products p LEFT JOIN sales s ON s.product_id=p.id GROUP BY p.id,p.name ORDER BY p.name;', 'Keyboard|150\nMonitor|400\nMouse|125\nStand|75'),

]



# ---------------------------------------------------------------------------
# PROBLEM TITLES
# ---------------------------------------------------------------------------

def _titles():
    return {

        "c": [
            ("Pointer Walk Sum", "Pointers"),
            ("In-place Array Shift", "Arrays"),
            ("String Length Without strlen", "Strings"),
            ("Reverse Text With Pointers", "Pointers"),
            ("Count Vowels In Buffer", "Strings"),
            ("Second Largest With One Pass", "Arrays"),
            ("Remove Duplicate Integers", "Arrays"),
            ("Selection Sort Trace", "Sorting"),
            ("Binary Search Function", "Searching"),
            ("Recursive Digit Sum", "Recursion"),
            ("Recursive Power", "Recursion"),
            ("Prime Check Function", "Functions"),
            ("GCD With Euclid", "Functions"),
            ("Matrix Diagonal Total", "Matrices"),
            ("Transpose A Square Matrix", "Matrices"),
            ("Character Frequency Table", "Strings"),
            ("Palindrome Buffer Check", "Strings"),
            ("Merge Two Sorted Arrays", "Arrays"),
            ("Rotate Array Right", "Arrays"),
            ("Maximum Subarray Sum", "Algorithms"),
            ("Bit Count Of An Integer", "Bitwise"),
            ("Toggle A Bit", "Bitwise"),
            ("Set And Clear A Bit", "Bitwise"),
            ("Swap Using Pointers", "Pointers"),
            ("Structure Sorting By Score", "Structures"),
            ("Student Average From Structs", "Structures"),
            ("Recursive Array Maximum", "Recursion"),
            ("Count Set Bits Recursively", "Recursion"),
            ("Fibonacci With Memo Array", "Dynamic Programming"),
            ("Stack Using Fixed Array", "Data Structures"),
            ("Queue Using Circular Array", "Data Structures"),
            ("Tokenize Words Manually", "Strings"),
            ("Compare Strings Without strcmp", "Strings"),
            ("Find First Unique Character", "Strings"),
            ("Frequency-Based Array Compression", "Arrays"),            ('Sum Even Elements', 'Arrays'),
            ('Count Positive Values', 'Arrays'),
            ('Reverse Integer Digits', 'Math'),
            ('Count Words In Line', 'Strings'),
            ('Find Minimum Value', 'Arrays'),
            ('Sum Digits Until Input Ends', 'Math'),
            ('Check Leap Year', 'Conditionals'),
            ('Remove Spaces From Text', 'Strings'),
            ('Merge Two Sorted Sequences', 'Arrays'),
            ('Count Character Occurrences', 'Strings'),

        ],

        "cpp": [
            ("Vector Prefix Totals", "STL Vector"),
            ("Rotate Vector Using STL", "STL Algorithms"),
            ("Erase Duplicate Values", "STL Set"),
            ("Frequency Map Of Scores", "STL Map"),
            ("First Repeated Number", "STL Unordered Map"),
            ("Top K Scores With Priority Queue", "Heap"),
            ("Kth Smallest With Multiset", "Multiset"),
            ("Queue Simulation", "Queue"),
            ("Deque Window Maximum", "Deque"),
            ("Stack Bracket Validator", "Stack"),
            ("Next Greater Element", "Stack"),
            ("Merge Intervals With Vector", "Intervals"),
            ("Custom Sort By Frequency", "Custom Comparator"),
            ("Pair Sum With Two Pointers", "Two Pointers"),
            ("Longest Unique Segment", "Strings"),
            ("Anagram Groups Signature", "Hashing"),
            ("Word Length Histogram", "Strings"),
            ("Lexicographically Smallest Rotation", "Strings"),
            ("Matrix Spiral Traversal", "Matrices"),
            ("Diagonal Difference", "Matrices"),
            ("DSU Component Counter", "Disjoint Set"),
            ("BFS Grid Distance", "Graphs"),
            ("DFS Connected Regions", "Graphs"),
            ("Dijkstra Small Graph", "Graphs"),
            ("Topological Course Order", "Graphs"),
            ("Coin Change Minimum", "Dynamic Programming"),
            ("Longest Increasing Subsequence", "Dynamic Programming"),
            ("0/1 Knapsack Capacity", "Dynamic Programming"),
            ("Binary Tree Level Width", "Trees"),
            ("BST Range Sum", "BST"),
            ("Heap Median Stream", "Heaps"),
            ("Sliding Window Distinct Count", "Sliding Window"),
            ("Prefix XOR Queries", "Bitwise"),
            ("Bitwise Unique Number", "Bitwise"),
            ("Interval Scheduling Count", "Greedy"),
            ("STL Lower Bound Position", "Searching"),
            ("String Compression Runs", "Strings"),
            ("Cyclic String Match", "Strings"),
            ("Ordered Set Rank Queries", "STL Set"),
            ("Map Merge With Maximum Value", "STL Map"),            ('Balanced Parentheses Checker', 'Stack'),
            ('Merge Two Sorted Vectors', 'Two Pointers'),
            ('Rotate Matrix Clockwise', 'Matrices'),
            ('Longest Word In Sentence', 'Strings'),
            ('Count Islands In Grid', 'Graphs'),
            ('Minimum Coins For Amount', 'Dynamic Programming'),
            ('Activity Selection', 'Greedy'),
            ('Find Peak Element', 'Binary Search'),
            ('Evaluate Postfix Expression', 'Stack'),
            ('Unique Paths In Grid', 'Dynamic Programming'),

        ],

        "java": [
            ("ArrayList Score Filter", "ArrayList"),
            ("HashMap First Duplicate", "HashMap"),
            ("HashSet Distinct Count", "HashSet"),
            ("TreeSet Sorted Distinct", "TreeSet"),
            ("PriorityQueue Top Scores", "PriorityQueue"),
            ("ArrayDeque Sliding Window", "Deque"),
            ("Stack Expression Depth", "Stack"),
            ("StringBuilder Reverse Words", "StringBuilder"),
            ("Character Frequency With Map", "HashMap"),
            ("Comparator Sort Students", "Comparator"),
            ("Immutable List Transformation", "Collections"),
            ("Stream Even Sum", "Streams"),
            ("Stream Group By Length", "Streams"),
            ("Optional First Match", "Optional"),
            ("Queue Round Robin", "Queue"),
            ("LinkedHashMap Order Tracking", "LinkedHashMap"),
            ("TreeMap Range Query", "TreeMap"),
            ("Merge Two Sorted Lists", "Lists"),
            ("Rotate Array Utility", "Arrays"),
            ("Binary Search Utility", "Arrays"),
            ("Matrix Row Totals", "Matrices"),
            ("Matrix Border Sum", "Matrices"),
            ("Recursive Factorial", "Recursion"),
            ("Memoized Fibonacci", "Dynamic Programming"),
            ("GCD Utility Method", "Methods"),
            ("Prime Sieve", "Arrays"),
            ("Longest Common Prefix", "Strings"),
            ("Palindrome With Character API", "Strings"),
            ("Anagram Normalizer", "Strings"),
            ("Word Frequency Ranking", "Maps"),
            ("LRU Cache Simulation", "LinkedHashMap"),
            ("Graph BFS With ArrayDeque", "Graphs"),
            ("Graph DFS With Recursion", "Graphs"),
            ("Connected Components", "Graphs"),
            ("Coin Change DP", "Dynamic Programming"),
            ("House Robber DP", "Dynamic Programming"),
            ("Binary Tree Height", "Trees"),
            ("BST Search", "Trees"),
            ("Comparable Score Ranking", "Comparator"),
            ("Exception-Safe Parser", "Exceptions"),            ('Count Even Digits', 'Math'),
            ('Reverse Word Order', 'Strings'),
            ('First NonRepeating Character', 'HashMap'),
            ('Merge Overlapping Intervals', 'Intervals'),
            ('Binary Tree Node Count', 'Trees'),
            ('Queue Using Two Stacks', 'Stacks'),
            ('Longest Palindromic Substring Length', 'Dynamic Programming'),
            ('Minimum Difference Pair', 'Sorting'),
            ('Top K Frequent Numbers', 'HashMap'),
            ('Valid Anagram Check', 'Strings'),

        ],

        "python": [
            ("List Comprehension Filter", "Lists"),
            ("Dictionary Inversion", "Dictionaries"),
            ("Set Difference Report", "Sets"),
            ("Counter Most Common", "Collections"),
            ("defaultdict Grouping", "Collections"),
            ("Deque Rotation", "Deque"),
            ("Tuple Record Sorting", "Tuples"),
            ("Enumerate Indexed Match", "Iteration"),
            ("Zip Column Totals", "Iteration"),
            ("Generator Running Total", "Generators"),
            ("Slicing Palindrome", "Strings"),
            ("F-String Formatter", "Strings"),
            ("Regex Digit Extractor", "Regex"),
            ("Regex Email Counter", "Regex"),
            ("Any/All Validation", "Built-ins"),
            ("Map Filter Pipeline", "Functional"),
            ("Reduce Product", "Functional"),
            ("Recursive Flatten", "Recursion"),
            ("Memoized Fibonacci", "Functools"),
            ("Binary Search With bisect", "Bisect"),
            ("Heapq Top K", "Heapq"),
            ("Ordered Dict Cache", "Dictionaries"),
            ("Prefix Sum Queries", "Algorithms"),
            ("Two Pointer Pair Count", "Algorithms"),
            ("Sliding Window Maximum", "Algorithms"),
            ("Matrix Transpose Comprehension", "Lists"),
            ("Spiral Matrix", "Matrices"),
            ("Word Frequency Ranking", "Dictionaries"),
            ("First Non-Repeating Character", "Strings"),
            ("Run Length Encoding", "Strings"),
            ("Prime Sieve With Slice Assignment", "Lists"),
            ("GCD With math.gcd", "Math"),
            ("LCM Batch With math.lcm", "Math"),
            ("Date Difference", "Datetime"),
            ("JSON Key Aggregation", "JSON"),
            ("CSV Score Average", "CSV"),
            ("Callable Validator", "Functions"),
            ("Decorator Call Counter", "Decorators"),
            ("Exception-Safe Conversion", "Exceptions"),
            ("Dataclass Record Ranking", "Dataclasses"),            ('Count Vowels In Text', 'Strings'),
            ('Preserve First Occurrences', 'Sets'),
            ('Longest Consecutive Ones', 'Arrays'),
            ('Group Anagrams', 'Hashing'),
            ('Merge Sorted Lists', 'Two Pointers'),
            ('Minimum Window Sum', 'Sliding Window'),
            ('Balanced Brackets', 'Stack'),
            ('Second Smallest Distinct', 'Sorting'),
            ('Matrix Row Sums', 'Matrices'),
            ('Common Elements Across Three Lists', 'Sets'),

        ],

        "javascript": [
            ("Map Frequency Counter", "Map"),
            ("Set Distinct Stream", "Set"),
            ("Reduce Transaction Total", "Array Reduce"),
            ("Find Duplicate With Set", "Set"),
            ("Group Scores By Range", "Map"),
            ("Sort Objects By Score", "Objects"),
            ("Destructure Coordinate Records", "ES6"),
            ("Rest Parameter Maximum", "Functions"),
            ("Spread Merge Unique", "ES6"),
            ("Arrow Function Pipeline", "Functions"),
            ("String Code Point Counter", "Strings"),
            ("Template Literal Formatter", "Strings"),
            ("Regex Digit Extractor", "Regex"),
            ("Regex URL Counter", "Regex"),
            ("Array Flat Nested Sum", "Arrays"),
            ("FlatMap Tokenizer", "Arrays"),
            ("Every/Some Validation", "Arrays"),
            ("Find Last Matching Index", "Arrays"),
            ("Binary Search Function", "Searching"),
            ("Stable Merge Sort", "Sorting"),
            ("Sliding Window Maximum", "Algorithms"),
            ("Two Pointer Pair Count", "Algorithms"),
            ("Prefix Sum Queries", "Algorithms"),
            ("LRU Cache Map", "Map"),
            ("Priority Queue Simulation", "Heap"),
            ("Matrix Spiral Traversal", "Matrices"),
            ("Graph BFS With Map", "Graphs"),
            ("Graph DFS With Set", "Graphs"),
            ("Topological Order", "Graphs"),
            ("Memoized Fibonacci", "Dynamic Programming"),            ('Count Vowels', 'Strings'),
            ('Remove Duplicate Words', 'Set'),
            ('Maximum Adjacent Difference', 'Arrays'),
            ('Chunk Array', 'Arrays'),
            ('Character Frequency Signature', 'Map'),

        ],

        "sql": [
            ("Department Salary Totals", "GROUP BY"),
            ("Employees Above Department Average", "Subquery"),
            ("Second Highest Salary", "ORDER BY"),
            ("Duplicate Email Detector", "GROUP BY"),
            ("Monthly Revenue Summary", "GROUP BY"),
            ("Customers Without Orders", "LEFT JOIN"),
            ("Employees With Managers", "SELF JOIN"),
            ("Top Earner Per Department", "Window Functions"),
            ("Running Revenue Total", "Window Functions"),
            ("Rank Products By Sales", "RANK"),
            ("Consecutive Login Days", "CTE"),
            ("First Order Per Customer", "ROW_NUMBER"),
            ("Latest Status Per Ticket", "Window Functions"),
            ("Average Salary By Role", "AVG"),
            ("Conditional Salary Bands", "CASE"),
            ("Null Safe Department Label", "COALESCE"),
            ("Join Three Business Tables", "JOIN"),
            ("Products Never Sold", "NOT EXISTS"),
            ("Orders Above Customer Average", "Correlated Subquery"),
            ("Duplicate Transaction Groups", "GROUP BY"),
            ("Seven Day Rolling Average", "Window Functions"),
            ("Percent Of Department Total", "Window Functions"),
            ("Customers With Multiple Orders", "HAVING"),
            ("Pivot Status Counts", "CASE"),
            ("Median Salary By Department", "Window Functions"),            ('Departments With More Than One Employee', 'GROUP BY'),
            ('Paid Revenue By Customer', 'JOIN'),
            ('Largest Order', 'ORDER BY'),
            ('Customers With Open Tickets', 'JOIN'),
            ('Product Sales Revenue', 'JOIN'),

        ],
    }


# ---------------------------------------------------------------------------
# DESCRIPTION
# ---------------------------------------------------------------------------

def _description(lang, title, topic, idx):
    return (
        f"Solve **{title}** as a {lang} placement coding problem. "
        f"The task focuses on {topic}. "
        f"Read the supplied input from standard input and print exactly "
        f"the required result. Handle edge cases and avoid hard-coding "
        f"the sample. Variant {idx + 1} is intentionally distinct "
        f"in data and requirement wording."
    )


# ---------------------------------------------------------------------------
# CREATE PROBLEM
# ---------------------------------------------------------------------------

def _make_problem(lang, title, topic, idx):

    # SQL problems
    if lang == "SQL":

        # IMPORTANT:
        # SQL_TASKS and SQL titles must have matching indexes.
        if idx >= len(SQL_TASKS):
            raise ValueError(
                f"Not enough SQL_TASKS entries for SQL problem index {idx}. "
                f"Available SQL tasks: {len(SQL_TASKS)}"
            )

        _, q, expected = SQL_TASKS[idx]

        return CodingProblem(
            title=title,
            difficulty=["Easy", "Medium", "Hard"][idx % 3],
            description=_description(lang, title, topic, idx),
            starter_code=q,
            tags=topic.lower().replace(" ", "-"),
            input_format="The temporary SQLite fixture is loaded automatically.",
            output_format="Return the requested rows in the stated order.",
            constraints="Use standard SQLite-compatible SQL.",
            examples=(
                "Schema and sample data are loaded automatically.\n"
                "Expected result:\n" + expected
            ),
            solution_reference=q,
            time_limit_ms=2000,
            memory_limit_mb=128,
            placement_level=['Basic','Intermediate','Advanced'][idx % 3],
            category=['General Placement','Service-based','Product-based','Interview Practice'][idx % 4]
        )

    # Non-SQL problems
    inp, out = _io_case(lang, idx)

    diff = ["Easy", "Medium", "Hard"][idx % 3]

    starter = _starter(lang, idx)

    # Language-specific reference snippet.
    ref = starter.replace(
        "TODO: implement the problem",
        "Reference implementation placeholder for the configured task"
    )

    ex = (
        f"Input:\n{inp.strip()}\n\n"
        f"Output:\n{out}"
    )

    return CodingProblem(
        title=title,
        difficulty=diff,
        description=_description(lang, title, topic, idx),
        starter_code=starter,
        tags=topic.lower().replace(" ", "-"),
        input_format="Standard input as shown in the example.",
        output_format="Print the exact expected value/sequence.",
        constraints="Use efficient time and memory for placement-sized input.",
        examples=ex,
        solution_reference=ref,
        time_limit_ms=2000,
        memory_limit_mb=128
    )



# ---------------------------------------------------------------------------
# EXTRA CURATED CASES
# ---------------------------------------------------------------------------
EXTRA_CASES = {
    "C · Sum Even Elements": [("6\n1 2 4 5 6 9\n","12"),("5\n8 3 10 2 7\n","20")],
    "C · Count Positive Values": [("6\n-2 4 0 3 -1 5\n","3"),("5\n1 -4 7 2 -8\n","3")],
    "C · Reverse Integer Digits": [("12030\n","3021"),("4500\n","54")],
    "C · Count Words In Line": [("hello world from placeprep\n","4"),("coding makes placements easier\n","4")],
    "C · Find Minimum Value": [("6\n8 3 9 1 4 2\n","1"),("5\n-2 7 -9 4 0\n","-9")],
    "C · Sum Digits Until Input Ends": [("12 34 5\n","15"),("99 8\n","26")],
    "C · Check Leap Year": [("2024\n","YES"),("1900\n","NO")],
    "C · Remove Spaces From Text": [("place prep code lab\n","placeprepcodelab"),("hello world\n","helloworld")],
    "C · Merge Two Sorted Sequences": [("3\n1 4 7\n4\n2 3 5 8\n","1 2 3 4 5 7 8"),("2\n0 9\n3\n1 2 10\n","0 1 2 9 10")],
    "C · Count Character Occurrences": [("banana\na\n","3"),("mississippi\ns\n","4")],

    "C++ · Balanced Parentheses Checker": [("(a+[b])\n","YES"),("([)]\n","NO")],
    "C++ · Merge Two Sorted Vectors": [("3\n1 4 7\n4\n2 3 5 8\n","1 2 3 4 5 7 8"),("2\n0 9\n3\n1 2 10\n","0 1 2 9 10")],
    "C++ · Rotate Matrix Clockwise": [("2\n1 2\n3 4\n","3 1\n4 2"),("3\n1 2 3\n4 5 6\n7 8 9\n","7 4 1\n8 5 2\n9 6 3")],
    "C++ · Longest Word In Sentence": [("I love competitive programming\n","competitive"),("PlacePrep helps students prepare\n","students")],
    "C++ · Count Islands In Grid": [("3 4\n1 1 0 0\n0 1 0 1\n1 0 0 1\n","3"),("2 3\n1 0 1\n0 1 0\n","3")],
    "C++ · Minimum Coins For Amount": [("11\n1 2 5\n","3"),("6\n1 3 4\n","2")],
    "C++ · Activity Selection": [("6\n1 2\n3 4\n0 6\n5 7\n8 9\n5 9\n","4"),("4\n1 3\n2 5\n4 6\n6 7\n","3")],
    "C++ · Find Peak Element": [("4\n1 2 3 1\n","2"),("5\n1 2 1 3 5\n","1")],
    "C++ · Evaluate Postfix Expression": [("2 3 + 4 *\n","20"),("5 1 2 + 4 * + 3 -\n","14")],
    "C++ · Unique Paths In Grid": [("3 7\n","28"),("3 3\n","6")],

    "Java · Count Even Digits": [("1203456\n","4"),("24680\n","5")],
    "Java · Reverse Word Order": [("I love coding\n","coding love I"),("PlacePrep makes learning easy\n","easy learning makes PlacePrep")],
    "Java · First NonRepeating Character": [("swiss\n","w"),("aabbcdde\n","c")],
    "Java · Merge Overlapping Intervals": [("3\n1 3\n2 6\n8 10\n","1 6\n8 10"),("4\n1 4\n4 5\n7 9\n8 10\n","1 5\n7 10")],
    "Java · Binary Tree Node Count": [("7\n1 2 3 4 5 -1 -1\n","5"),("3\n1 2 3\n","3")],
    "Java · Queue Using Two Stacks": [("6\nENQ 10\nENQ 20\nDEQ\nENQ 30\nDEQ\nDEQ\n","10 20 30"),("5\nENQ 4\nDEQ\nENQ 9\nENQ 8\nDEQ\n","4 9")],
    "Java · Longest Palindromic Substring Length": [("babad\n","3"),("cbbd\n","2")],
    "Java · Minimum Difference Pair": [("5\n8 1 5 12 4\n","1"),("4\n20 3 9 15\n","6")],
    "Java · Top K Frequent Numbers": [("7 2\n1 1 1 2 2 3 3\n","1 2"),("6 2\n4 4 5 5 5 6\n","5 4")],
    "Java · Valid Anagram Check": [("listen silent\n","YES"),("hello world\n","NO")],

    "Python · Count Vowels In Text": [("PlacePrep Coding Arena\n","8"),("Education is important\n","10")],
    "Python · Preserve First Occurrences": [("8\n4 2 4 3 2 1 3 5\n","4 2 3 1 5"),("6\na b a c b d\n","a b c d")],
    "Python · Longest Consecutive Ones": [("8\n1 1 0 1 1 1 0 1\n","3"),("6\n0 1 1 1 1 0\n","4")],
    "Python · Group Anagrams": [("6\nact cat dog tac god tca\n","act cat tac\ndog god"),("5\neat tea tan ate nat\n","eat tea ate\ntan nat")],
    "Python · Merge Sorted Lists": [("3\n1 4 7\n4\n2 3 5 8\n","1 2 3 4 5 7 8"),("2\n0 9\n3\n1 2 10\n","0 1 2 9 10")],
    "Python · Minimum Window Sum": [("5 3\n4 2 7 1 3\n","10"),("6 2\n5 1 4 2 8 3\n","3")],
    "Python · Balanced Brackets": [("{[()]}\n","YES"),("([)]\n","NO")],
    "Python · Second Smallest Distinct": [("7\n5 1 2 2 8 1 3\n","2"),("5\n9 9 7 8 7\n","8")],
    "Python · Matrix Row Sums": [("3 3\n1 2 3\n4 5 6\n7 8 9\n","6 15 24"),("2 4\n1 1 1 1\n2 3 4 5\n","4 14")],
    "Python · Common Elements Across Three Lists": [("5\n1 2 3 4 5\n4\n2 3 5 7\n4\n0 2 3 9\n","2 3"),("3\n1 4 7\n3\n2 4 6\n3\n0 4 8\n","4")],

    "JavaScript · Count Vowels": [("Hello PlacePrep\n","4"),("Programming\n","3")],
    "JavaScript · Remove Duplicate Words": [("8\ncode learn code practice learn code test practice\n","code learn practice test"),("5\none two two three one\n","one two three")],
    "JavaScript · Maximum Adjacent Difference": [("5\n10 3 8 20 15\n","12"),("4\n1 9 2 7\n","8")],
    "JavaScript · Chunk Array": [("7 3\n1 2 3 4 5 6 7\n","1 2 3\n4 5 6\n7"),("5 2\na b c d e\n","a b\nc d\ne")],
    "JavaScript · Character Frequency Signature": [("banana\n","a:3 b:1 n:2"),("hello\n","e:1 h:1 l:2 o:1")],
}

# ---------------------------------------------------------------------------
# SEED CODING BANK
# ---------------------------------------------------------------------------

def seed_coding_bank():

    names = {
        "c": "C",
        "cpp": "C++",
        "java": "Java",
        "python": "Python",
        "javascript": "JavaScript",
        "sql": "SQL"
    }

    icons = {
        "c": "terminal",
        "cpp": "code-2",
        "java": "coffee",
        "python": "braces",
        "javascript": "file-code-2",
        "sql": "database"
    }

    all_titles = _titles()

    for slug, name in names.items():

        lang = CodingLanguage.query.filter_by(slug=slug).first()

        if not lang:
            lang = CodingLanguage(
                name=name,
                slug=slug,
                icon=icons[slug]
            )

            db.session.add(lang)
            db.session.flush()

        titles = all_titles[slug]

        # Safety check for SQL: every SQL title must have exactly one
        # matching SQL task/query.
        if slug == "sql" and len(titles) != len(SQL_TASKS):
            raise ValueError(
                f"SQL title count ({len(titles)}) does not match "
                f"SQL task count ({len(SQL_TASKS)})."
            )

        for idx, (title, topic) in enumerate(titles):

            full = f"{name} · {title}"

            # Don't duplicate existing problems.
            existing = CodingProblem.query.filter_by(
                title=full, language_id=lang.id
            ).first()
            if existing:
                existing.placement_level = ['Basic','Intermediate','Advanced'][idx % 3]
                existing.category = ['General Placement','Service-based','Product-based','Interview Practice'][idx % 4]
                # Repair/refresh test data for the curated SQL and newly-added
                # language-specific problems when an older PlacePrep database
                # is upgraded in place.
                if slug == 'sql':
                    _, _, expected = SQL_TASKS[idx]
                    cases = sorted(existing.test_cases, key=lambda c: c.id)
                    for case in cases:
                        case.input = SQL_FIXTURE
                        case.expected_output = expected.replace('\\n', '\n')
                    if not cases:
                        db.session.add(CodingTestCase(problem=existing, input=SQL_FIXTURE,
                                                      expected_output=expected.replace('\\n','\n'), hidden=False))
                        db.session.add(CodingTestCase(problem=existing, input=SQL_FIXTURE,
                                                      expected_output=expected.replace('\\n','\n'), hidden=True))
                elif full in EXTRA_CASES:
                    cases = sorted(existing.test_cases, key=lambda c: c.id)
                    if len(cases) >= 2:
                        cases[0].input, cases[0].expected_output = EXTRA_CASES[full][0]
                        cases[0].hidden = False
                        cases[1].input, cases[1].expected_output = EXTRA_CASES[full][1]
                        cases[1].hidden = True
                continue

            p = _make_problem(
                name,
                title,
                topic,
                idx
            )

            p.title = full
            p.language = lang

            db.session.add(p)
            db.session.flush()

            # -----------------------------------------------------------
            # SQL TEST CASES
            # -----------------------------------------------------------
            if slug == "sql":

                # One SQL title maps to exactly one SQL task.
                _, sql_query, expected = SQL_TASKS[idx]

                inp = SQL_FIXTURE
                out = expected.replace('\\n', '\n')

                hidden_inp = SQL_FIXTURE
                hidden_out = expected.replace('\\n', '\n')

            # -----------------------------------------------------------
            # OTHER LANGUAGE TEST CASES
            # -----------------------------------------------------------
            else:

                extra = EXTRA_CASES.get(full)
                if extra:
                    inp, out = extra[0]
                    hidden_inp, hidden_out = extra[1]
                else:
                    inp, out = _io_case(slug, idx)
                    # Keep the existing bank deterministic while ensuring the
                    # generated hidden case is different from the visible case.
                    hidden_inp, hidden_out = _io_case(slug, (idx + 7) % 35)

            # Public test case
            db.session.add(
                CodingTestCase(
                    problem=p,
                    input=inp,
                    expected_output=out,
                    hidden=False
                )
            )

            # Hidden test case
            db.session.add(
                CodingTestCase(
                    problem=p,
                    input=hidden_inp,
                    expected_output=hidden_out,
                    hidden=True
                )
            )

        # Update language problem count.
        lang.problem_count = CodingProblem.query.filter_by(
            language_id=lang.id
        ).count()

    db.session.commit()