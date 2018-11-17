import requests
import json

print ("Hello World")

url = "http://www.apilayer.net/api/live?access_key=df1fa21b42994013fed11d8454508658&format=1"
response = requests.get(url)

convert_from = str(input("IDR/CAD/AUD/PLN/USD:"))
convert_to = str(input("IDR/CAD/AUD/PLN/USD:"))
amount = float(input("amount of money to convert:"))
convert_from = "USD" + convert_from
convert_to = "USD" + convert_to


if response.status_code != 200:
    print("error {}".format(response.status_code))
else:
    data = json.loads(response.text)
    # for key,row in data["quotes"].items():
    #     print (key)
    #     print(row)

    if convert_from == "USDUSD":
        if convert_to in data["quotes"]:
            USD_currency = float(data["quotes"][convert_to])
            total = "%.2f" % round(USD_currency * amount, 2)
            print("total converted amount:", total)
    elif convert_from != "USDUSD":
        if convert_from and convert_to in data["quotes"]:
            from_number = float(data["quotes"][convert_from])
            to_number = float(data["quotes"][convert_to])
            # ratio_number = from_number / to_number
            total3 = "%.2f" % round(to_number / from_number* amount, 2)
            print("total converted amount:", total3)

