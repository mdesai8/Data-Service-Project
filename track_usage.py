import shelve

USAGE_FILE_PATH = "numUsages"

def create_file():

    usages = shelve.open(USAGE_FILE_PATH, flag='n')

    usages['life_expectancy'] = 0
    usages['gdp'] = 0
    usages['labour'] = 0
    usages['co2'] = 0
    usages['fertility_rate'] = 0

    usages.close()


def getNumUsages(endpoint):

    try:
        usages = shelve.open(USAGE_FILE_PATH, flag='r')
    except:
        create_file()
        usages = shelve.open(USAGE_FILE_PATH, flag='r')

    if endpoint in usages:
        return usages[endpoint]

    return 0

def incrementUsage(endpoint):
    try:
        usages = shelve.open(USAGE_FILE_PATH, flag='w')
    except:
        create_file()
        usages = shelve.open(USAGE_FILE_PATH, flag='w')

    currUsages = usages[endpoint]
    usages[endpoint] = currUsages + 1

    usages.close()
