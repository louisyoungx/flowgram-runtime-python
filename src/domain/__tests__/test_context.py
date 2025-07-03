"""
Test script for the workflow runtime context.
"""
import json
from typing import Dict, Any

from ...interface.schema import InvokeParams
from ..context import WorkflowRuntimeContext


def test_context_creation():
    """
    Test the creation of a workflow runtime context.
    """
    # Create a context
    context = WorkflowRuntimeContext.create()
    
    # Verify that the context is not None
    assert context is not None
    
    # Verify that the context has all the required components
    assert context.document is not None
    assert context.variable_store is not None
    assert context.state is not None
    assert context.io_center is not None
    assert context.snapshot_center is not None
    assert context.status_center is not None
    assert context.reporter is not None
    
    print("Context creation test passed.")


def test_context_initialization():
    """
    Test the initialization of a workflow runtime context.
    """
    # Create a context
    context = WorkflowRuntimeContext.create()
    
    # Create invoke parameters
    params: InvokeParams = {
        "schema": {
            "nodes": [],
            "edges": []
        },
        "inputs": {
            "input1": "value1",
            "input2": "value2"
        }
    }
    
    # Initialize the context
    context.init(params)
    
    print("Context initialization test passed.")


def test_context_sub():
    """
    Test the creation of a sub-context.
    """
    # Create a context
    context = WorkflowRuntimeContext.create()
    
    # Create a sub-context
    sub_context = context.sub()
    
    # Verify that the sub-context is not None
    assert sub_context is not None
    
    # Verify that the sub-context has all the required components
    assert sub_context.document is not None
    assert sub_context.variable_store is not None
    assert sub_context.state is not None
    assert sub_context.io_center is not None
    assert sub_context.snapshot_center is not None
    assert sub_context.status_center is not None
    assert sub_context.reporter is not None
    
    print("Sub-context creation test passed.")


def test_context_variable_store():
    """
    Test the variable store of a workflow runtime context.
    """
    # Create a context
    context = WorkflowRuntimeContext.create()
    
    # Initialize the context
    params: InvokeParams = {
        "schema": {
            "nodes": [],
            "edges": []
        },
        "inputs": {}
    }
    context.init(params)
    
    # Set a variable
    context.variable_store.set("key1", "value1")
    
    # Verify that the variable exists
    assert context.variable_store.has("key1")
    
    # Verify that the variable has the correct value
    assert context.variable_store.get("key1") == "value1"
    
    # Delete the variable
    context.variable_store.delete("key1")
    
    # Verify that the variable no longer exists
    assert not context.variable_store.has("key1")
    
    print("Variable store test passed.")


def test_context_variable_store_inheritance():
    """
    Test the variable store inheritance of a workflow runtime context.
    """
    # Create a context
    context = WorkflowRuntimeContext.create()
    
    # Initialize the context
    params: InvokeParams = {
        "schema": {
            "nodes": [],
            "edges": []
        },
        "inputs": {}
    }
    context.init(params)
    
    # Set a variable in the parent context
    context.variable_store.set("key1", "value1")
    
    # Create a sub-context
    sub_context = context.sub()
    
    # Verify that the variable exists in the sub-context
    assert sub_context.variable_store.has("key1")
    
    # Verify that the variable has the correct value in the sub-context
    assert sub_context.variable_store.get("key1") == "value1"
    
    # Set a variable in the sub-context
    sub_context.variable_store.set("key2", "value2")
    
    # Verify that the variable exists in the sub-context
    assert sub_context.variable_store.has("key2")
    
    # Verify that the variable does not exist in the parent context
    assert not context.variable_store.has("key2")
    
    print("Variable store inheritance test passed.")


def test_context_disposal():
    """
    Test the disposal of a workflow runtime context.
    """
    # Create a context
    context = WorkflowRuntimeContext.create()
    
    # Initialize the context
    params: InvokeParams = {
        "schema": {
            "nodes": [],
            "edges": []
        },
        "inputs": {}
    }
    context.init(params)
    
    # Create a sub-context
    sub_context = context.sub()
    
    # Dispose the context
    context.dispose()
    
    print("Context disposal test passed.")


def main():
    """
    Main function to run all tests.
    """
    print("Running context tests...")
    
    test_context_creation()
    test_context_initialization()
    test_context_sub()
    test_context_variable_store()
    test_context_variable_store_inheritance()
    test_context_disposal()
    
    print("All context tests passed.")


if __name__ == "__main__":
    main()