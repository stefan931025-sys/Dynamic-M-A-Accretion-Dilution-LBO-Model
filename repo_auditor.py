#!/usr/bin/env python3
"""
Repository Structural and AST Auditor (`repo_auditor.py`)
Enforces structural hygiene, AST-based code patterns, and compliance standards
across the multi-repository quantitative development lifecycle.
"""

import ast
import sys
import os
from pathlib import Path

# Define mandatory directories and files for structural compliance
MANDATORY_DIRS = ['src', 'tests', '.github/workflows']
MANDATORY_FILES = ['README.md', 'requirements.txt', '.gitignore']


class ASTCodeAuditor(ast.NodeVisitor):
    """AST-based static analyzer to enforce safe coding practices and quantitative rigor."""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.errors = []
        self.warnings = []

    def visit_Call(self, node):
        # 1. Detect unsafe builtins
        if isinstance(node.func, ast.Name):
            if node.func.id == 'eval':
                self.errors.append(f"{self.filepath}:{node.lineno}: Security violation: Use of 'eval()' is strictly prohibited.")
            elif node.func.id == 'exec':
                self.errors.append(f"{self.filepath}:{node.lineno}: Security violation: Use of 'exec()' is strictly prohibited.")
        
        # 2. Detect unseeded random number generation calls
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id in ('random', 'np', 'numpy') and 'rand' in node.func.attr:
                self.warnings.append(f"{self.filepath}:{node.lineno}: Quantitative warning: Unseeded random call '{node.func.value.id}.{node.func.attr}()' detected. Use a seeded Generator for reproducibility.")

        self.generic_visit(node)

    def visit_Compare(self, node):
        # 3. Detect floating-point direct equality checks (Eq / NotEq)
        for op in node.ops:
            if isinstance(op, (ast.Eq, ast.NotEq)):
                self.warnings.append(f"{self.filepath}:{node.lineno}: Quantitative warning: Direct float equality/inequality comparison detected. Use math.isclose() or np.isclose().")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Check if public functions have docstrings
        if not ast.get_docstring(node) and not node.name.startswith('_'):
            self.warnings.append(f"{self.filepath}:{node.lineno}: Style warning: Public function '{node.name}' lacks a docstring.")
        self.generic_visit(node)


def audit_repository(root_dir='.'):
    root = Path(root_dir)
    print(f"[*] Starting repository audit for: {root.resolve()}")
    
    failed = False
    
    # 1. Check Mandatory Directory Structure
    print("[*] Auditing directory structure...")
    for d in MANDATORY_DIRS:
        dir_path = root / d
        if not dir_path.is_dir():
            print(f"  [X] Missing mandatory directory: {d}/")
            failed = True
        else:
            print(f"  [✓] Found directory: {d}/")

    # 2. Check Mandatory Files
    print("[*] Auditing mandatory configuration files...")
    for f in MANDATORY_FILES:
        file_path = root / f
        if not file_path.is_file():
            print(f"  [X] Missing mandatory file: {f}")
            failed = True
        else:
            print(f"  [✓] Found file: {f}")

    # 3. Run AST & Static Analysis on Python Files
    print("[*] Running AST linting and static analysis on Python sources...")
    python_files = list(root.glob('**/*.py'))
    
    # Exclude virtual environments or build artifacts
    python_files = [p for p in python_files if not any(part.startswith('.') or part in ['venv', 'build', 'dist'] for part in p.parts)]

    total_errors = 0
    total_warnings = 0

    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content, filename=str(py_file))
            
            auditor = ASTCodeAuditor(py_file)
            auditor.visit(tree)
            
            for err in auditor.errors:
                print(f"  [ERROR] {err}")
                total_errors += 1
            for warn in auditor.warnings:
                print(f"  [WARNING] {warn}")
                total_warnings += 1
                
        except SyntaxError as se:
            print(f"  [SYNTAX ERROR] {py_file}:{se.lineno}: {se.msg}")
            total_errors += 1
        except Exception as e:
            print(f"  [ERROR] Failed to parse {py_file}: {e}")
            total_errors += 1

    print(f"\n[*] Audit Summary: {total_errors} errors, {total_warnings} warnings found.")

    if failed or total_errors > 0:
        print("[!] Repository audit FAILED. Please resolve structural or AST errors before building.")
        sys.exit(1)
    else:
        print("[✓] Repository audit PASSED successfully. Codebase complies with governance standards.")
        sys.exit(0)


if __name__ == '__main__':
    target_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    audit_repository(target_directory)
