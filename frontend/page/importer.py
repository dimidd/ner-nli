import json
import os.path

from entities.models import Entity
from . import models


def import_result(base, entity_id, entity_type, entity_alias,
                  entity_alias_count, entity_lookup, words):

    assert len(words), "No words supplied"

    # get or create a Book
    book_path = os.path.dirname(words[0]['PAGE_FILE'])
    if book_path.startswith('books2/'):
        book_path = book_path[7:]
    book = models.Book.objects.get_or_create(
            path=book_path,
            defaults={'title': 'A book'}
    )[0]

    # get or create a Page
    ordinal = base.split("-")[-1]
    page = models.Page.objects.get_or_create(
            book=book,
            ordinal=ordinal,
            path=base,
    )[0]

    # get or create an Entity
    entity = Entity.objects.get_or_create(
            control_number=entity_id,
            type=Entity.Types.from_code.get(entity_type),
            hebrew_alias=entity_alias,
    )[0]

    # (get or) create an Hit
    models.Hit.objects.get_or_create(
            entity=entity,
            page=page,
            content=" ".join([word['CONTENT'] for word in words]),
            word_count=len(words),
            first_word_id=words[0]['ID'],
            alto_info=json.dumps(
                    [{
                         'block': word['GRANDPARENT'],
                         'id': word['ID'],
                         'content': word['CONTENT']
                     } for word in words]
            )
    )
    return 1
