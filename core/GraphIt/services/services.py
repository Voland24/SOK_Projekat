from abc import ABC, abstractmethod

from GraphIt.models import Graph


class AbstractService(ABC):
    """Abstract class that models the interface for plugins"""

    @abstractmethod
    def identification(self) -> str:
        """Unique identification for this plugin"""
        pass

    @abstractmethod
    def name(self) -> str:
        """Name used to recognize this plugin"""
        pass


class DataSourceService(AbstractService):
    """Abstract class that models the interface for data source plugins"""

    @abstractmethod
    def load_data(self, resource: str) -> Graph:
        """Function that returns the data parsed as a Graph"""
        pass


class GraphViewService(AbstractService):
    """Abstract class that models the interface for graph view plugins"""

    @abstractmethod
    def get_script_path(self) -> str:
        """Function that returns javascript file path"""
        pass

    def get_vertices(self) -> list:
        """Function that returns list of vertices"""
        return self.graph.vertices()

    def get_edges(self) -> list:
        """Function that returns list of edges"""
        return self.graph.edges()
