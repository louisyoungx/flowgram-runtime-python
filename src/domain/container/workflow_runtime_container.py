"""
Container for workflow runtime services.
"""
from typing import Dict, Any, TypeVar, Type, cast, Callable

from ...interface import IContainer, IEngine, IExecutor, IValidation
from ...domain.validation import WorkflowRuntimeValidation
from ...domain.executor import WorkflowRuntimeExecutor
from ...domain.engine import WorkflowRuntimeEngine
from ...nodes import WorkflowRuntimeNodeExecutors

T = TypeVar('T')
ContainerService = Any


class WorkflowRuntimeContainer(IContainer):
    """
    Container for workflow runtime services.
    Implements the IContainer interface to provide access to services.
    """
    
    _instance = None
    
    def __init__(self, services: Dict[Any, ContainerService]):
        """
        Initialize the container with services.
        
        Args:
            services: A dictionary mapping service keys to service instances.
        """
        self._services = services
        self._factories = {}
        self._singletons = {}
    
    def get(self, key: Type[T]) -> T:
        """
        Get a service by key.
        
        Args:
            key: The key of the service to get.
            
        Returns:
            The service instance.
        """
        # Check if key exists in services
        if key in self._services:
            return cast(T, self._services[key])
        
        # Check if key exists in singletons
        if key in self._singletons:
            factory = self._singletons[key]
            instance = factory()
            self._services[key] = instance
            return cast(T, instance)
        
        # Check if key exists in factories
        if key in self._factories:
            factory = self._factories[key]
            return cast(T, factory())
        
        raise KeyError(f"Service not found: {key}")
    
    def register(self, key: Any, instance: T) -> None:
        """
        Register an instance for a dependency key.
        
        Args:
            key: The dependency key.
            instance: The dependency instance.
        """
        self._services[key] = instance
    
    def register_factory(self, key: Any, factory: Callable[[], T]) -> None:
        """
        Register a factory function for a dependency key.
        
        Args:
            key: The dependency key.
            factory: The factory function that creates the dependency instance.
        """
        self._factories[key] = factory
    
    def register_singleton(self, key: Any, factory: Callable[[], T]) -> None:
        """
        Register a singleton factory function for a dependency key.
        
        Args:
            key: The dependency key.
            factory: The factory function that creates the singleton dependency instance.
        """
        self._singletons[key] = factory
    
    @classmethod
    def instance(cls) -> 'WorkflowRuntimeContainer':
        """
        Get the singleton instance of the container.
        
        Returns:
            The singleton instance of the container.
        """
        if cls._instance is None:
            services = cls._create()
            cls._instance = WorkflowRuntimeContainer(services)
        return cls._instance
    
    @classmethod
    def _create(cls) -> Dict[Any, ContainerService]:
        """
        Create the services for the container.
        
        Returns:
            A dictionary mapping service keys to service instances.
        """
        # Create services
        validation = WorkflowRuntimeValidation()
        executor = WorkflowRuntimeExecutor(WorkflowRuntimeNodeExecutors)
        engine = WorkflowRuntimeEngine({
            "Executor": executor,
        })
        
        # Return services
        return {
            IValidation: validation,
            IExecutor: executor,
            IEngine: engine,
        }
