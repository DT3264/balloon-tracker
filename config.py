# *********************************
# *****     GENERAL STUFF     *****
# *********************************

## The platform to use
## [ OMEGAUP | CODEFORCES ]
PLATFORM = "OMEGAUP"

## Seconds to wait between each request for new data
SECONDS_INTERVAL = 30


# *********************************
# *****     OMEGAUP STUFF     *****
# *********************************
OMEGAUP = {
    # The alias of the contest (also known as titulo corto), also is the contest path
    # omegaup.com/contest/{ALIAS}/
    'CONTEST_ALIAS': "CONTEST_ALIAS",
    # The omegaup api key that allows the requests to go through
    # You can find it by going to https://omegaup.com/profile/#manage-api-tokens
    'API_TOKEN': "YOUR_API_TOKEN"
}

# ************************************
# *****     CODEFORCES STUFF     *****
# ************************************
CODEFORCES = {
    'CONTEST_ID': "1804",
    # The API KEY & SECRET can be obtained here
    # https://codeforces.com/settings/api
    'API_KEY': "YOUR_API_KEY",
    'API_SECRET': "YOUR_API_SECRED",
    # If true, looks for the contest inside the group specified below
    # If false, looks for the contest in the public contests
    'IS_CONTEST_PRIVATE': False,
    # Group code to look for private contest (if IS_CONTEST_PRIVATE is True)
    'GROUP_CODE': "YOUR_GROUP_CODE",
}
