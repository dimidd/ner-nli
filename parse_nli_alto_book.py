from lxml import etree


def parse_file(filename):
    with open(filename, "rb") as f:
        tree = etree.parse(f)
    print(tree.getroot())
    for word in tree.xpath("//String[@CONTENT]"):
        print("ID:", word.get("ID"),
              "CONTENT:", word.get("CONTENT"),
              )


if __name__ == "__main__":
    parse_file("books_alto_fmt/1227225-140-0100.xml")  # page 100 from some book
