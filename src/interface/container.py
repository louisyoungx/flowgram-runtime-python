"""
Container interfaces for the runtime.
This module contains the interfaces for dependency injection container.
"""
from typing import Any, Dict, Generic, TypeVar
from abc import ABC, abstractmethod


T = TypeVar('T')


class IContainer(Generic[T], ABC):
    """
    Interface for dependency injection container.
    
    The container manages dependencies and provides instances of them.
    """
    
    @abstractmethod
    def get(self, key: Any) -> T:
        """
        Get an instance of a dependency.
        
        Args:
            key: The dependency key.
            
        Returns:
            The dependency instance.
        """
        pass
    
    @abstractmethod
    def register(self, key: Any, instance: T) -> None:
        """
        Register an instance for a dependency key.
        
        Args:
            key: The dependency key.
            instance: The dependency instance.
        """
        pass
    
    @abstractmethod
    def register_factory(self, key: Any, factory: Any) -> None:
        """
        Register a factory function for a dependency key.
        
        Args:
            key: The dependency key.
            factory: The factory function that creates the dependency instance.
        """
        pass
    
    @abstractmethod
    def register_singleton(self, key: Any, factory: Any) -> None:
        """
        Register a singleton factory function for a dependency key.
        
        Args:
            key: The dependency key.
            factory: The factory function that creates the singleton dependency instance.
        """
        pass
