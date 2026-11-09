"""Verify the Codex replication without modifying benchmark sources.

Run with python3 -B src/verify_codex_replication.py. Compilation uses temporary
directories. Embedded suites run once, with assertions enabled; saved benchmark
repetition counts remain untouched. Results are JSON on stdout.
"""

import ast
import copy
import functools
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from config.constants import PROGRAMS, LANGUAGES


def python_namespace(path):
    tree = ast.parse(path.read_text())
    tree.body = [node for node in tree.body if not (
        isinstance(node, ast.If) and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == '__name__'
    )]
    namespace = {'__name__': 'verification'}
    shim = not hasattr(functools, 'cache')
    if shim:
        functools.cache = functools.lru_cache(maxsize=None)
    try:
        exec(compile(tree, str(path), 'exec'), namespace)
    finally:
        if shim:
            del functools.cache
    return namespace


def command(argv, cwd):
    try:
        run = subprocess.run(argv, cwd=str(cwd), capture_output=True, timeout=120)
        return {'returncode': run.returncode, 'stdout': run.stdout.decode(errors='replace'),
                'stderr': run.stderr.decode(errors='replace')}
    except subprocess.TimeoutExpired:
        return {'returncode': 'timeout', 'stdout': '', 'stderr': '120-second timeout'}


def check(path, repair_declaration=False):
    if path.suffix == '.py':
        try:
            ns = python_namespace(path)
            ns['testSolution'](ns['Solution']())
            result = {'returncode': 0, 'stdout': '', 'stderr': ''}
        except Exception as exc:
            result = {'returncode': type(exc).__name__, 'stdout': '', 'stderr': str(exc)}
        if sys.version_info < (3, 9) and 'from functools import cache' in path.read_text():
            result['compatibility'] = 'functools.cache verified using equivalent lru_cache(maxsize=None) shim'
        return result
    with tempfile.TemporaryDirectory(prefix='codex-check-') as temp:
        build = Path(temp)
        text = path.read_text()
        if repair_declaration:
            text = text.replace('public class Solution', 'class Solution')
        text, reduced = re.subn(
            r'(for\s*\(int i\s*=\s*0;\s*i\s*<\s*)\d+'
            r'(;\s*(?:\+\+i|i\+\+)\)\s*\{?\s*\n?\s*(?:testSolution|runTests))',
            r'\g<1>1\2', text)
        if reduced > 1:
            raise ValueError('Unexpected multiple repeated-test loops in ' + str(path))
        source = build / path.name
        source.write_text(text)
        cpp = path.suffix == '.cpp'
        compile_result = command(['g++', '-O2', '-std=c++17', str(source), '-o', str(build / 'program')]
                                 if cpp else ['javac', str(source)], build)
        if compile_result['returncode']:
            return dict(compile_result, phase='compile')
        return dict(command([str(build / 'program')] if cpp else
                            ['java', '-ea', '-cp', str(build), path.stem], build), phase='assertions')


def cases(name, rng):
    if name == 'N-Queens':
        return 'solveNQueens', [(i,) for i in range(9)]
    if name == 'Sudoku_Solver':
        solved = [[str((r * 3 + r // 3 + c) % 9 + 1) for c in range(9)] for r in range(9)]
        boards = []
        for _ in range(50):
            board = copy.deepcopy(solved)
            for r, c in rng.sample([(r, c) for r in range(9) for c in range(9)], rng.randrange(25)):
                board[r][c] = '.'
            boards.append((board,))
        return 'solveSudoku', boards
    if name == 'Median_of_Two_Sorted_Arrays':
        pairs = [(sorted(rng.choices(range(-20, 21), k=rng.randrange(10))),
                  sorted(rng.choices(range(-20, 21), k=rng.randrange(10)))) for _ in range(200)]
        return 'findMedianSortedArrays', [p for p in pairs if p[0] or p[1]]
    if name in ('Trapping_Rain_Water', 'Largest_Rectangle_in_Histogram', 'First_Missing_Positive'):
        method = {'Trapping_Rain_Water': 'trap', 'Largest_Rectangle_in_Histogram': 'largestRectangleArea',
                  'First_Missing_Positive': 'firstMissingPositive'}[name]
        low = -10 if name == 'First_Missing_Positive' else 0
        return method, [(rng.choices(range(low, 21), k=rng.randrange(25)),) for _ in range(200)]
    if name == 'Regular_Expression_Matching':
        return 'isMatch', [(''.join(rng.choices('ab', k=rng.randrange(8))),
                            ''.join(rng.choice('ab.') + rng.choice(('', '*')) for _ in range(rng.randrange(7))))
                           for _ in range(200)]
    if name == 'Find_Edges_in_Shortest_Paths':
        result = []
        for _ in range(100):
            n = rng.randrange(1, 12)
            result.append((n, [[u, v, rng.randrange(1, 15)] for u in range(n) for v in range(u + 1, n)
                               if rng.random() < 0.3]))
        return 'findAnswer', result
    if name == 'Length_of_the_Longest_Increasing_Path':
        result = []
        for _ in range(100):
            n = rng.randrange(1, 30)
            result.append(([[rng.randrange(20), rng.randrange(20)] for _ in range(n)], rng.randrange(n)))
        return 'maxPathLength', result
    if name == 'Minimum_Window_Substring':
        return 'minWindow', [(''.join(rng.choices('abc', k=rng.randrange(25))),
                              ''.join(rng.choices('abc', k=rng.randrange(1, 8)))) for _ in range(200)]
    if name == 'Permutation_Sequence':
        import math
        return 'getPermutation', [(n, rng.randrange(1, math.factorial(n) + 1))
                                  for n in range(1, 9) for _ in range(20)]
    if name == 'Sorted_GCD_Pair_Queries':
        result = []
        for _ in range(100):
            n = rng.randrange(2, 15)
            result.append((rng.choices(range(1, 40), k=n), [rng.randrange(n * (n - 1) // 2) for _ in range(10)]))
        return 'gcdValues', result
    if name == 'Find_Number_of_Coins_to_Place_in_Tree_Nodes':
        result = []
        for _ in range(100):
            n = rng.randrange(1, 20)
            result.append(([[rng.randrange(i), i] for i in range(1, n)], rng.choices(range(-9, 10), k=n)))
        return 'placedCoins', result
    if name == 'Text_Justification':
        return 'fullJustify', [([''.join(rng.choices('abc', k=rng.randrange(1, 9)))
                                for _ in range(rng.randrange(20))], rng.randrange(8, 25)) for _ in range(100)]
    if name == 'Find_the_Sum_of_Subsequence_Powers':
        result = []
        for _ in range(100):
            n = rng.randrange(2, 9)
            result.append((rng.choices(range(-10, 20), k=n), rng.randrange(2, n + 1)))
        return 'sumOfPowers', result
    return None, []


def outcome(namespace, method, arguments):
    args = copy.deepcopy(arguments)
    try:
        return ('returned', getattr(namespace['Solution'](), method)(*args), args)
    except Exception as exc:
        return ('raised', type(exc).__name__, str(exc), args)


def linked_checks(name, human, codex, rng):
    count = 0
    for _ in range(100):
        values = [sorted(rng.choices(range(-5, 6), k=rng.randrange(12))) for _ in range(rng.randrange(10))]
        if name == 'Reverse_Nodes_in_k-Group':
            values = [rng.choices(range(-5, 6), k=rng.randrange(30))]
        k = rng.randrange(1, 10)
        results = []
        for ns in (human, codex):
            heads = []
            for group, array in enumerate(values):
                head = None
                for index in reversed(range(len(array))):
                    node = ns['ListNode'](array[index])
                    node.next, node.tag = head, (group, index)
                    head = node
                heads.append(head)
            solution = ns['Solution']()
            node = solution.mergeKLists(heads) if name == 'Merge_k_Sorted_Lists' else solution.reverseKGroup(heads[0], k)
            output = []
            seen = set()
            while node is not None:
                if id(node) in seen:
                    raise AssertionError('Cycle in linked-list result')
                seen.add(id(node))
                output.append((node.val, node.tag))
                node = node.next
            results.append(output)
        if results[0] != results[1]:
            raise AssertionError((name, values, k, results))
        count += 1
    return count


def matches_baseline(record):
    baseline = record.get('human_with_declaration_repair', record['human'])
    variant = record['codex']
    if baseline['returncode'] != variant['returncode'] or baseline['stdout'] != variant['stdout']:
        return False
    if variant['returncode'] == 0:
        return True
    if variant.get('phase') != 'assertions' or baseline.get('phase') != 'assertions':
        return False
    # Compare the failure cause, ignoring temporary paths and source line numbers.
    def cause(result):
        error = result['stderr']
        java = re.search(r'java\.lang\.\w+(?::[^\n]*)?', error)
        if java:
            return java.group(0)
        assertion = re.search(r'Test case \d+ failed\.', error)
        return assertion.group(0) if assertion else None
    return cause(baseline) is not None and cause(baseline) == cause(variant)


def main():
    records = []
    for program in PROGRAMS:
        for language in LANGUAGES:
            relative = Path(program['folder']) / program['files'][language]
            original, target = ROOT / 'src/data/human' / relative, ROOT / 'Results/code/codex' / relative
            record = {'problem': program['name'], 'language': language,
                      'human': check(original), 'codex': check(target),
                      'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
            if record['human'].get('phase') == 'compile' and 'public class Solution' in original.read_text():
                record['human_with_declaration_repair'] = check(original, repair_declaration=True)
            record['matches_baseline_after_documented_declaration_repair'] = matches_baseline(record)
            records.append(record)
            print(program['name'] + '/' + language + ': ' + str(record['codex']['returncode']), file=sys.stderr, flush=True)
    rng = random.Random(1729)
    differential = []
    for program in PROGRAMS:
        relative = Path(program['folder']) / program['files']['python']
        human = python_namespace(ROOT / 'src/data/human' / relative)
        codex = python_namespace(ROOT / 'Results/code/codex' / relative)
        name = program['name']
        if name in ('Merge_k_Sorted_Lists', 'Reverse_Nodes_in_k-Group'):
            count = linked_checks(name, human, codex, rng)
        else:
            method, inputs = cases(name, rng)
            for args in inputs:
                a, b = outcome(human, method, args), outcome(codex, method, args)
                if a != b:
                    raise AssertionError((name, args, a, b))
            count = len(inputs)
        differential.append({'problem': name, 'cases_passed': count})
    print(json.dumps({'mode': 'embedded assertions once; saved repetition loops unchanged',
                      'python': sys.version, 'variants': records, 'python_differential': differential}, indent=2))
    failures = {(r['problem'], r['language']) for r in records if r['codex']['returncode'] != 0}
    expected = {('Sudoku_Solver', 'java'), ('Merge_k_Sorted_Lists', 'java'),
                ('Find_the_Sum_of_Subsequence_Powers', 'cpp')}
    return 0 if failures == expected and all(matches_baseline(r) for r in records) else 1


if __name__ == '__main__':
    sys.exit(main())
