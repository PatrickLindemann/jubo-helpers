import argparse
from abc import ABC, abstractmethod


class Routine(ABC):

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this routine

        Returns
        -------
        str
            The name of this routine
        """
        pass

    @abstractmethod
    def get_parser(self) -> argparse.ArgumentParser:
        """Get the argument parser for the routine

        Returns
        -------
        argparse.ArgumentParser
            The argument parser
        """
        pass

    @abstractmethod
    def run(self, args: dict = {}):
        """Run the routine

        Parameters
        ----------
        args : dict, optional
            The arguments for this routine, by default {}
        """
        pass
