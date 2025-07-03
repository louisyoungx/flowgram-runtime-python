"""
Implementation of the workflow runtime IO center.

The IO center manages the inputs and outputs of the workflow. It stores the
input values provided when the workflow is invoked and collects the output
values produced during workflow execution. The outputs can be accessed after
the workflow has completed, providing the results of the workflow execution.

The IO center is initialized with the input values and maintains the output
values throughout the workflow execution.
"""
from typing import Any, Dict

from ...interface.context import IIOCenter


class WorkflowRuntimeIOCenter(IIOCenter):
    """
    Implementation of the IO center.
    This class manages inputs and outputs of the workflow.
    """

    def __init__(self):
        """
        Initialize a new instance of the WorkflowRuntimeIOCenter class.
        """
        self._inputs: Dict[str, Any] = {}
        self._outputs: Dict[str, Any] = {}

    @property
    def inputs(self) -> Dict[str, Any]:
        """
        Get the workflow inputs.
        
        Returns:
            The workflow inputs.
        """
        return self._inputs
    
    @property
    def outputs(self) -> Dict[str, Any]:
        """
        Get the workflow outputs.
        
        Returns:
            The workflow outputs.
        """
        return self._outputs

    def init(self, inputs: Dict[str, Any]) -> None:
        """
        Initialize the IO center with the given inputs.
        
        Args:
            inputs: The workflow inputs.
        """
        self._inputs = inputs
        self._outputs = {}
        
    def set_outputs(self, outputs: Dict[str, Any]) -> None:
        """
        Set the workflow outputs.
        
        Args:
            outputs: The workflow outputs.
        """
        self._outputs = outputs

    def dispose(self) -> None:
        """
        Dispose the IO center and release resources.
        """
        self._inputs = {}
        self._outputs = {}
