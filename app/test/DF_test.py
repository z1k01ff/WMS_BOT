import pandas as pd

data = {
      "nosiy": [100, 100, 100],
  "artikul": [110, 220, 110],
    "nazva": ["baunty", "snickers", "baunty"]
}

#load data into a DataFrame object:
df = pd.DataFrame(data)

result = []

for i in df["nazva"]:
    if i not in result:
        result.append(i)
print(result)

btn_soder_test = KeyboardButton('Тест')

vmist_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_soder_nisiy, btn_artikul, btn_nazva_artikulf, btn_soder_test, btn_back)

