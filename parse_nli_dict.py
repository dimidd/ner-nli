from lxml import etree


def clear_element(e):
    e.clear()
    while e.getprevious() is not None:
        del e.getparent()[0]


def parse_file(filename):
    with open(filename, "rb") as f:
        context = etree.iterparse(f,
                               tag="{http://www.loc.gov/MARC21/slim}record")
        for action, elem in context:
            parse_record(elem)
            clear_element(elem)


def parse_record(elem):
    print(elem.tag)
    # print(etree.tostring(elem))
    for x in elem:
        print(x)


parse_file("nnl10all_head.xml")
