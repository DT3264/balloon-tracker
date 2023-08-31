from typing import Dict

import requests

import config


class OmegaupFetcher:

    def __init__(self):
        self.contest_alias = config.OMEGAUP['CONTEST_ALIAS']
        self.problem_order: Dict[str, int] = {}
        self.headers = {
    'Authorization': f'token {config.OMEGAUP["API_TOKEN"]}'
}

    def fetch_ac_submissions(self) -> list[dict[str, int]]:
        url = 'https://omegaup.com/api/contest/runs/'
        exists_data = True
        ac_runs = []
        offset = 0
        # Keep requesting submissions while having data in the last request
        while exists_data:
            data = {
                'contest_alias': self.contest_alias,
                'show_all': 'true',
                'offset': offset,
            }
            response = requests.post(url, data, headers=self.headers).json()
            for run in response["runs"]:
                # Get the index of the problem
                problem_order = self.problem_order[run['alias']]
                if run["verdict"] == "AC":
                    # If AC, append to the runs
                    ac_runs.append({'username': run["username"], 'problem_order': problem_order})
            if len(response["runs"]) == 0:
                # If the response has no data, no need to look further
                exists_data = False
            offset += 1
        return ac_runs

    def get_initial_data(self):
        # Gets the scoreboard which has the amount of problems and the contestants
        url = "https://omegaup.com/api/contest/scoreboard/"
        data = {'contest_alias': self.contest_alias}
        response = requests.post(url, data, headers=self.headers).json()
        self.__prepare_problems_index(response)
        base_data = []
        # Array of 0s, meaning we have no data for that problem yet
        problems = [0] * len(response["problems"])

        # For each user, get their data and append it to the list
        for user in response["ranking"]:
            base_data.append({
                'username': user['username'],
                'user': user['name'],
                'problems': problems
            })
        return base_data

    def __prepare_problems_index(self, response):
        for problem in response["problems"]:
            # Matches the problem alias to the problem order
            self.problem_order[problem["alias"]] = int(problem["order"])
