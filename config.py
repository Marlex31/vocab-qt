from os import getcwd
import json


class Config():
    """Object that holds the info read from the config file"""

    def __init__(self, dark_theme=False, recent_files=[f"{getcwd()}\\vocabulary.csv", None, None], window_size=[0, 0, 640, 480]):
        super().__init__()

        try:
            with open('settings.json', 'r', encoding='utf8') as r:
                self.settings = json.load(r)


        except FileNotFoundError:

            filename = f'{getcwd()}\\vocabulary.csv'
            with open(filename, 'w', encoding='utf8') as w:
                writer(file=filename, data=[{'col_1':'lorem', 'col_2':'ipsum', 'col_3':'dolor'}])


            self.settings = {'dark_theme':dark_theme, 'recent_files':recent_files, 'window_size':window_size}
             
            with open('settings.json', 'w', encoding='utf8') as w:
                json.dump(self.settings, w)


        # attribute assignment
        self.dark_theme = self.settings['dark_theme']
        self.recent_files = self.settings['recent_files']
        self.window_size = tuple(self.settings['window_size'])


    def save(self, dark_theme, recent_files, window_size):

        for i in range(3): 
            if recent_files[0] == self.settings['recent_files'][0]:
                recent_files = self.settings['recent_files']
                break

            elif self.settings['recent_files'][i] not in recent_files and i <= 1:
                recent_files[i+1] = self.settings['recent_files'][i]

            elif i == 2:
                break

        self.settings = {'dark_theme':dark_theme, 'recent_files':recent_files, 'window_size':window_size}
        
        with open('settings.json', 'w', encoding='utf8') as w:
            json.dump(self.settings, w)

        
# c = Config()
# c.save()
# print(c.settings)
# print(c.window_size)

# from utilities import json_files

# print(json_files())