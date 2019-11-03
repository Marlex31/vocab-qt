import json

settings = {'first_launch':True, 'dark_theme':False, 'recent_files':[None, None, None]}

d1 = False
d2 = True
d3 = ['french.csv', 'comma_file.csv', None]
# settings.update(zip(settings.keys(), [d1,d2,d3]))

with open('settings.json', 'w') as w:
    json.dump(settings, w) # indent=2


with open('settings.json', 'r') as r:
    data = json.load(r)
    print(data)

