#! /usr/bin/python3
# coding=utf-8

from lxml import etree
from pprint import pprint
from pathlib import Path


def extract_words_from_alto_xml(filepath):
    """
    extract words from an xml file in alto format
    return list of words, each word is accompanied with metadata
    to locate its source

    """
    with filepath.open() as f:
        tree = etree.parse(f)
    words = []
    for word in tree.xpath("//String[@CONTENT]"):
        words.append({"ID": word.get("ID"),
                      "CONTENT": word.get("CONTENT"),
                      "PARENT": word.getparent().get("ID"),
                      "GRANDPARENT": word.getparent().getparent().get("ID"),
                      "PAGE_FILE": filepath,
                      })
    return words


def lookup(candidate, entities):
    """
        return first record in entities that match candidate
    """
    for record in entities:
        if candidate == record['name']:
            return record['id']
    return None


def slice(l, size):
    for i in range(len(l) + 1 - size):
        yield l[i:i+size]


def candidate2text(candidate):
    return ", ".join([w['CONTENT'] for w in candidate])


def generate_candidate_variants(candidate):
    just_the_words = [w['CONTENT'] for w in candidate]
    words_to_discard = [
        'את',
        'של',
        'על',
        'לא',
        'כי',
        'כל',
        'הוא',
        'עם',
        'גם',
        'זה',
        'אל',
        'ולא',
        'היה',
        'שלא',
        'לו',
        'זו',
        'אם',
        'אין',
        'מה',
        'בכל',
        'מן',
        'אחרי',
        'עד',
        'אלא',
        'רק',
        'אף',
        'אבל',
        'יש',
        'בין',
        'אנו',
        'עוד',
        'ביום',
        "עמ'",
        'נגד',
        'י',
        'אך',
        'הם',
        'היא',
        'או',
        'ראה',
        'כדי',
        ':',
        'להוסיף:',
        'אני',
        'אותו',
        'להם',
        'וראה',
        'אולם',
        'שאין',
        'כן',
        'אמר',
        'לפי',
        'ואל',
        'כמה',
        'באותו',
        'אליו',
        'שם',
        'מתוך',
        'מר',
        'לנו',
        'בו',
        'מי',
        'יותר',
        "גל'",
        'בת',
        'אינו',
        'כאשר',
        'אצל',
        'שום',
        'לכל',
        'כך',
        'ועל',
        "ה'",
        'אז',
        'שנה',
        'שהוא',
        'מפני',
        'היו',
        'כפי',
        'מאת',
        'וכל',
        'הרי',
        'היתה',
        'בפני',
        'מכל',
        'לי',
        'להלן',
        'זאת',
        'בענין',
        'צריך',
        'להיות',
        'הלא',
        'אחת',
        '1',
        '?',
        'פה',
        'זו,',
        'זה,',
        'ואין',
        'בעד',
        'אפילו',
        'עליו',
        'כבר',
        'וכן',
        'ואם',
        'הנ"ל',
        'בקרב',
        'בספר',
        'בהם',
        'אב',
        'עצמו',
        'מטעם',
        'מהם',
        'מ.',
        'לפניו',
        'כאילו',
        'בזה',
        'אסור',
        '*',
        '.',
        'שהיא',
        'יכול',
        'בשנת',
        'פח.',
        'לה',
        'חזר',
        'זה.',
        'אלה',
        '♦',
        '-',
    ]
    for w in just_the_words:
        if w in words_to_discard:
            return  # skip this candidate
    candidate_as_str = candidate2text(candidate)
    yield candidate_as_str
    candidate_as_str = candidate2text(candidate[::-1])
    yield candidate_as_str


def look_for_entities(words, entities):
    res = []
    query_count = 0
    for candidate in slice(words, 2):
        for candidate_as_str in generate_candidate_variants(candidate):
            query_count += 1
            t = lookup(candidate_as_str, entities)
            if t:
                res.append((t, candidate, candidate_as_str))
    print("number of queries: {}".format(query_count))
    return res


def gather_info_from_folder(path):
    folder = Path(path)
    res = []
    l = list(folder.glob('*.xml'))
    l = sorted(l)
    for f in l:
        words = extract_words_from_alto_xml(f)
        res += words
    return res


if __name__ == "__main__":
    path = "../nli_entities_sample_data/additional_books/IE26721743/REP26723234/"
    words = gather_info_from_folder(path)
    # pprint(res)
    entities = [
        {'id': 1, 'name': 'לחוק, התורהl', },
        {'id': 2, 'name': 'חייבים, לשמוע', },
        {'id': 3, 'name': 'ישראל, בניגוד', },
        {'id': 4, 'name': 'לחוק, בניגוד', },
        ]
    # TODO probably send source (name of file which contains page?) also
    res = look_for_entities(words, entities)
    print("number of result: {}".format(len(res)))
    pprint(res)
