import datetime


def normalize_date(doc):
    if isinstance(doc, datetime.date) and not isinstance(doc, datetime.datetime):
        doc = datetime.datetime.combine(doc, datetime.time.min)
    return doc
