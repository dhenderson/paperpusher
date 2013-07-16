import config

# open the test json file
data = config.load_json('test.json')

# save the data in the test json file
config.save_json('test.json', data)