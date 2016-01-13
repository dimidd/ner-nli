import bs4


def get_paragraphs(xml_filename, highlight_ids):
    with open(xml_filename) as f:
        bs = bs4.BeautifulSoup(f, "html.parser")

    # if xml contains multiple "Page" elements, it will only show the first one
    page = bs.alto.layout.page
    paragraphs = []
    paragraph = None
    line = None
    for printspace in page.findAll('printspace'):
        for textblock in printspace.findAll('textblock'):
            if paragraph is None:
                paragraph = []
            else:
                paragraphs.append(paragraph)
                paragraph = []
            for textline in textblock.findAll('textline'):
                if line is None:
                    line = []
                else:
                    paragraph.append(line)
                    line = []
                for string in textline.findAll('string'):
                    id = string['id']
                    if id in highlight_ids:
                        line.append(
                                '<span style="color:red"'
                                ' data-hit="{}" data-entity="{}"'
                                ' data-type="{}">{}</span>'.format(
                                        highlight_ids[id].id,
                                        highlight_ids[id].entity_id,
                                        highlight_ids[id].entity.type,
                                        string['content']
                                ))
                    else:
                        line.append(string['content'])
    paragraph.append(line)
    paragraphs.append(paragraph)

    return paragraphs
