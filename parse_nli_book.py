from lxml import etree


def parse_file(filename):
    with open(filename, "rb") as f:
        tree = etree.parse(f)
    print(tree.getroot())
    for div in tree.xpath("//def:div[@LABEL]",
                          namespaces={'def': 'http://www.loc.gov/METS/'}):
        print("TYPE:", div.get("TYPE"),
              "ORDER:", div.get("ORDER"),
              "LABEL:", div.get("LABEL"))


if __name__ == "__main__":
    # parse_file("books_fmt/2704714-10-TEXT_utf8.xml")  # book in French
    parse_file("books_fmt/2696068-10-TEXT_utf8.xml")  # book in English
