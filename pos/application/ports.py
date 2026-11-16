from abc import ABC, abstractmethod


class ExportPort(ABC):

    @abstractmethod
    def export(self, rows, filename):
        pass
