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
    'CONTEST_ALIAS': "ccms2023",
    # The omegaup cookie that allows the requests to go through
    # You can find it by going to the omegaup cookies in the developer tools
    'OUAT': "2b6d20441d8bb6b494f79b76a88298-13814-1caec061c653ef21d1fab068a253fe7087c30317c862e85d79927f6bd7e58a11"
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
