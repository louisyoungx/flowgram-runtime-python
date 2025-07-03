"""
Validation interfaces for the workflow runtime.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, TypedDict

from .schema import WorkflowSchema


class ValidationResult(TypedDict):
    """
    Result of a workflow schema validation.
    """
    valid: bool
    errors: Dict[str, Any] | None


class IValidation(ABC):
    """
    Interface for workflow schema validation.
    """
    
    @abstractmethod
    def validate(self, schema: WorkflowSchema) -> ValidationResult:
        """
        Validates a workflow schema.
        
        Args:
            schema: The workflow schema to validate.
            
        Returns:
            A validation result object.
        """
        pass