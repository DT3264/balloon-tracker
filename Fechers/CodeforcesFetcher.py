import requests
import hashlib
import time

import config
from Fechers.BaseFetcher import BaseFetcher


class CodeforcesFetcher(BaseFetcher):

    def __init__(self):
        self.api_key = "82f97dcd775b56c62a0f2ecf2973301910740383"
        self.api_secret = "17b440fbddbf9099eafc75f42b07a47e9b1f05ed"

        self.cf_api = CodeforcesAPI(
            config.CODEFORCES['CONTEST_ID'],
            config.CODEFORCES['API_KEY'],
            config.CODEFORCES['API_SECRET'],
            is_contest_private=config.CODEFORCES['IS_CONTEST_PRIVATE'],
            group_code=config.CODEFORCES['GROUP_CODE'],
        )

    def get_initial_data(self) -> list[dict[str, list[int]]]:
        # Gets the scoreboard which has the amount of problems and the contestants
        return self.cf_api.get_contest_data()

    def fetch_ac_submissions(self) -> list[dict[str, int]]:
        return self.cf_api.get_ac_submissions()


def build_headers():
    return {"Content-Type": "text/plain"}


class CodeforcesAPI:
    def __init__(self, contest_id, api_key, api_secret, group_code=None, is_contest_private=False):
        self.contest_id = contest_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.group_code = group_code
        self.is_private = is_contest_private

    def build_params(self, method):
        if not self.is_private:
            return {"contestId": self.contest_id}
        rand = "123456"
        time_now = str(int(time.time()))
        str_ = f"{rand}/{method}?apiKey={self.api_key}&contestId={self.contest_id}&groupCode={self.group_code}&time={time_now}#{self.api_secret}"
        hash_ = hashlib.sha512(str_.encode('utf-8')).hexdigest()
        return {
            "groupCode": self.group_code,
            "contestId": self.contest_id,
            "apiKey": self.api_key,
            "time": time_now,
            "apiSig": rand + hash_
        }

    def get_ac_submissions(self):
        url = "https://codeforces.com/api/contest.status"
        response = requests.get(url, headers=build_headers(), params=self.build_params("contest.status")).json()
        return [
            {
                "username": submission["author"]["members"][0]["handle"],
                "problem_order": ord(submission["problem"]["index"]) - 65,
            }
            for submission in response["result"]
            if submission["verdict"] == "OK"
        ]

    def get_contest_data(self):
        url = "https://codeforces.com/api/contest.standings"
        response = requests.get(url, headers=build_headers(), params=self.build_params("contest.standings", )).json()
        problems = [0] * len(response['result']['problems'])
        contestants = [{
            'username': row['party'].get('teamName') or row['party']['members'][0]['handle'],
            'problems': problems
        } for row in response['result']['rows']]
        return contestants
