import bs4
from django.core.urlresolvers import reverse


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
                        url = reverse("entity_detail", args=(highlight_ids[id].entity_id,))
                        line.append(
                                '<a href="{}" '
                                ' data-hit="{}" data-entity="{}"'
                                ' class="entity-{}">{}</a>'.format(
                                        url,
                                        highlight_ids[id].id,
                                        highlight_ids[id].entity_id,
                                        highlight_ids[id].entity.type_code(),
                                        string['content']
                                ))
                    else:
                        line.append(string['content'])
    paragraph.append(line)
    paragraphs.append(paragraph)

    return paragraphs
