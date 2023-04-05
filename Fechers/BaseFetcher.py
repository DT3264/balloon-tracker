from abc import ABC, abstractmethod


class BaseFetcher(ABC):
    # Method to get the initial data (teams and the amount of problems)
    # For example:
    # [
    #   {'username': 'SomeUser', 'problems': [0,0,0,0]},
    #   {'username': 'AnotherUser', 'problems': [0,0,0,0]}
    # ]
    # problems is the state of the problems which is
    # 0 -> Unsolved / 1 -> Solved / 2-> Balloon already given
    @abstractmethod
    def get_initial_data(self) -> list[dict[str, list[int]]]:
        pass

    # Method to retrieve correct submissions
    # For example:
    # [{'username': 'SomeUser', 'problem_order': 0}]
    # problem_order is the index of the solved problem 0-indexed
    @abstractmethod
    def fetch_ac_submissions(self) -> list[dict[str, int]]:
        pass
