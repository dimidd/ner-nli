#! /usr/bin/python3
# coding=utf-8

import re
from lxml import etree
from pprint import pprint
from pathlib import Path
import db_api
import sys

chars_to_remove = re.compile(r'[-:+/_־—,\'".!.)(~*©§■•|}{£«□¥#♦^<>?✓=;\\[\]]+')


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
        words.append({
            "ID": word.get("ID"),
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
        yield l[i:i + size]


def candidate2text(candidate):
    return " ".join([w for w in candidate])


def remove_special_chars(candidate_as_str):
    temp_str = chars_to_remove.sub(' ', candidate_as_str)
    return re.sub(r' +', ' ', temp_str.strip())


def generate_candidate_variants(candidate):
    just_the_words = [remove_special_chars(w['CONTENT']) for w in candidate]
    if len(just_the_words) == 1:
        if len(just_the_words[0].split()) < 2:
            return
    words_to_discard = [
        '',
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
        'יום',
    ]

    for w in just_the_words:
        if w in words_to_discard:
            return  # skip this candidate
    candidate_as_str = candidate2text(just_the_words)
    candidates = set()
    candidates.add(candidate_as_str)
    candidate_as_str = candidate2text(just_the_words[::-1])
    candidates.add(candidate_as_str)
    for i in candidates:
        yield i


MAX_WORDS_IN_QUERY = 6  # should be 32 for current max alias in NLI entities...


def look_for_entities(words, entities):
    res = []
    query_count = 0
    word_index = 0
    while word_index < len(words):
        for slice_length in range(MAX_WORDS_IN_QUERY, 0, -1):
            candidate = words[word_index:word_index + slice_length]
            # print(candidate)
            res_for_candidate = []
            for candidate_str in generate_candidate_variants(candidate):
                # print(candidate_as_str)
                query_count += 1
                t = lookup(candidate_str, entities)
                t = db_api.lookup(candidate_str)
                # if t:
                #     res_for_candidate.append((t, candidate, candidate_str))
                for r in t:
                    res.append((r['id'], r["aliases"][0], candidate, candidate_str))
            if res_for_candidate:  # found at least one match so skip over all words in it
                res.extend(res_for_candidate)
                word_index += slice_length
                break
        else:  # no matches found that start at currnt word
            word_index += 1
    print("number of queries: {}".format(query_count))
    return res


def gather_info_from_folder(path, page=-1):
    folder = Path(path)
    res = []
    l = list(folder.glob('*.xml'))
    l = sorted(l)
    if page != -1:
        page_ind = page - 1
        if page_ind < 0 or page_ind >= len(l):
            print("Wrong page")
            sys.exit(1)
        f = l[page_ind]
        words = extract_words_from_alto_xml(f)
        res += words
    else:
        for f in l:
            words = extract_words_from_alto_xml(f)
            res += words
    return res


if __name__ == "__main__":
    path = "books2/IE26721743/REP26723234/"
    if len(sys.argv) > 1:
        page = int(sys.argv[1])
    else:
        page = -1
    words = gather_info_from_folder(path, page)

    entities = [
        {'id': 1, 'name': 'לחוק התורהl', },
        {'id': 2, 'name': 'חייבים לשמוע', },
        {'id': 3, 'name': 'ישראל בניגוד', },
        {'id': 4, 'name': 'לחוק בניגוד', },
        {'id': 5, 'name': 'יונתן בן עוזיאל', },
    ]
    # TODO probably send source (name of file which contains page?) also
    res = look_for_entities(words, entities)
    print("number of results: {}".format(len(res)))
    pprint(res)
