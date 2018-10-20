import webbrowser

user = "shopify"
url = "https://www.instagram.com/" + user + "/?__a=1"

chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

webbrowser.get(chrome_path).open(url)
