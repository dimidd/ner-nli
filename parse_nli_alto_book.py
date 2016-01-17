#! /usr/bin/python3
# coding=utf-8

import re
from lxml import etree
from pprint import pprint
from pathlib import Path
import db_api
import sys
import copy

CHARS_TO_REMOVE = '[-:+/_־—,\'".!.)(~*©§■•|}{£«□¥#♦^<>?✓=;\\[\]]+'
CHARS_TO_REMOVE_REGEX = re.compile(CHARS_TO_REMOVE)


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
    temp_str = CHARS_TO_REMOVE_REGEX.sub(' ', candidate_as_str)
    return re.sub(r' +', ' ', temp_str.strip())


def generate_candidate_variants(candidate):
    just_the_words = [remove_special_chars(w['CONTENT']) for w in candidate]
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
    ]

    for w in just_the_words:
        if w in words_to_discard:
            return  # skip this candidate

    candidate_as_str = candidate2text(just_the_words)
    candidates = set()
    dash = r'-|־'

    candidates = candidates.union(prefix(candidate_as_str))
    candidate_as_str = candidate2text(just_the_words[::-1])
    candidates = candidates.union(prefix(candidate_as_str))
    for w in candidate[0:1]:
        content = w['CONTENT']
        if re.search(dash, content):
            candidates.add(content)
            content_dashless = re.sub(dash, ' ', content)
            candidates.add(content_dashless)
            content = content_dashless
        if content.find(' ') > -1:
            candidates.add(content)
            candidates = candidates.union(prefix(content))

    for i in candidates:
        yield i

PREFIXES = ['ה', 'ו', 'ל', 'מ', 'ב', 'כ', 'ש']
PREFIXES2 = [
    'ול', 'ומ', 'וב', 'וכ', 'וש', 'וה',
    'מה',
    'שה', 'של', 'שמ', 'שב', 'שכ', 'שכ'
]
PREFIXES3 = [
    'וכש', 'שכש', 'לכש', 'ולכש',
    'ומה', 'ושה', 'כשה', 'וכשה',
    'לכשה', 'ולכשה', 'ומש', 'ומשה'
]


def prefix(s):
    res = find_prefix(s, PREFIXES)
    if len(res) == 0:
        res = find_prefix(s, PREFIXES2)
    if len(res) == 0:
        res = find_prefix(s, PREFIXES3)

    return res


def find_prefix(s, l):
    res = set()
    res.add(s)
    for p in l:
        if s.startswith(p):
            res.add(s[len(p):])

    return res

SPELLINGS = {'שרות': 'שירות'}


def check_spell(cand):
    for w in cand:
        if w['CONTENT'] in SPELLINGS:
            w['CONTENT'] = SPELLINGS[w['CONTENT']]

    return cand


def traverse_cand_strs(cand_strs, cand, no_other=True):
    res = []
    query_count = 0
    for cs in cand_strs:
        query_count += 1
        t = db_api.lookup(cs, no_other)
        for r in t:
            res.append(
                (
                    int(r['id']),
                    r['type'],
                    r['aliases'][0],
                    len(r['aliases']),
                    cs,
                    cand
                )
            )

    return (res, query_count)


def look_for_entities(words, entities):
    res = []
    query_count = 0
    for candidate in slice(words, 2):
        cand_strs = generate_candidate_variants(candidate)
        (cur_res, cur_query_count) = traverse_cand_strs(cand_strs, candidate)
        query_count += cur_query_count
        res += cur_res
        if len(cur_res) == 0:
            alt_cand = check_spell(candidate)
            cand_strs = generate_candidate_variants(alt_cand)
            (cur_res, cur_query_count) = traverse_cand_strs(
                                            cand_strs, candidate, False
                                        )
            query_count += cur_query_count
            res += cur_res

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


def remove_dupes(res):
    new_res = []
    can_set = set()
    max_size = -1
    for r in res:
        alias = (r[1], r[2])
        if alias in can_set:
            if r[3] > max_size:
                new_res[:] = [x for x in new_res if not (x[1], x[2]) == alias]
                can_set.add(alias)
                new_res.append(r)
        else:
            new_res.append(r)
            can_set.add(alias)

    return new_res

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
    res = remove_dupes(res)
    print("number of results: {}".format(len(res)))
    pprint(res)
