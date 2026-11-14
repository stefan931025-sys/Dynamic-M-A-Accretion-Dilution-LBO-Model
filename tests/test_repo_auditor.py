"""
Unit Tests for AST Code Auditor (`tests/test_repo_auditor.py`)
"""

import ast
import pytest
from pathlib import Path
import sys

# Import the AST auditor class from parent or src
# (Assuming repo_auditor.py is in the root or accessible path)
sys.path.append(str(Path(__file__).parent.parent))
from repo_auditor import ASTCodeAuditor


def test_ast_detects_float_equality():
    """Verify that direct float equality (==) triggers a warning."""
    code = """
def check_price(p):
    if p == 100.50:
        return True
    return False
    """
    tree = ast.parse(code)
    auditor = ASTCodeAuditor("mock_file.py")
    auditor.visit(tree)
    
    assert len(auditor.warnings) > 0
    assert any("Direct float equality" in warning for warning in auditor.warnings)


def test_ast_detects_unseeded_random():
    """Verify that unseeded random calls trigger a warning."""
    code = """
import random
def get_noise():
    return random.random()
    """
    tree = ast.parse(code)
    auditor = ASTCodeAuditor("mock_file.py")
    auditor.visit(tree)
    
    assert len(auditor.warnings) > 0
    assert any("Unseeded random call" in warning for warning in auditor.warnings)
