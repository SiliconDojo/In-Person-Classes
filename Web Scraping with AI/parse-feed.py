import feedparser

d = feedparser.parse("https://feeds.arstechnica.com/arstechnica/index")

# print(d)

for value in d.entries:
    print(value.title)
    print(value.links[0].href)
    print(value.description)
    print("*******")
