"""
Test schemas package.

This package contains schema definitions for testing workflow execution.
"""
from .basic import basic_schema
from .basic_llm import basic_llm_schema
from .branch import branch_schema
from .loop import loop_schema
from .two_llm import two_llm_schema

# Export all schemas as a class for easy access
class TestSchemas:
    """Collection of test schemas."""
    basic_schema = basic_schema
    basic_llm_schema = basic_llm_schema
    branch_schema = branch_schema
    loop_schema = loop_schema
    two_llm_schema = two_llm_schema

__all__ = ['TestSchemas', 'basic_schema', 'basic_llm_schema', 'branch_schema', 'loop_schema', 'two_llm_schema']