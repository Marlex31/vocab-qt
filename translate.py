from googletrans import Translator

translator = Translator()

result = translator.translate('bonjour', src='fr', dest='ro')

print(result.text)