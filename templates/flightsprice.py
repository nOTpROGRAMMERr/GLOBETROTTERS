import requests

# url = "https://compare-flight-prices.p.rapidapi.com/GetPricesAPI/StartFlightSearch.aspx"
#
# querystring = {"lapinfant":"0","child":"0","city2":"DAD","date1":"2024-06-06","youth":"2","flightType":"2","adults":"2","cabin":"1","infant":"0","city1":"BOM","seniors":"0","date2":"2024-06-10"}
#
# headers = {
# 	"X-RapidAPI-Key": "d612f1772bmsh0ace657eb36ea5ep18f1d4jsna2686512fe13",
# 	"X-RapidAPI-Host": "compare-flight-prices.p.rapidapi.com"
# }
#
# response = requests.get(url, headers=headers, params=querystring)
#
# print(response.json())



url = "https://compare-flight-prices.p.rapidapi.com/GetPricesAPI/GetPrices.aspx"

querystring = {"SearchID":"vietnam"}

headers = {
	"X-RapidAPI-Key": "d612f1772bmsh0ace657eb36ea5ep18f1d4jsna2686512fe13",
	"X-RapidAPI-Host": "compare-flight-prices.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())