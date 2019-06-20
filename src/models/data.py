import mongoengine as me


class JobDescription(me.Document):

    jd_id = me.StringField(required=True)
    jd_title = me.StringField(required=True)
    jd_html = me.StringField(required=True)
    jd_sentences = me.ListField(required=True)

    meta = {
        'indexes': ['jd_id'],
        'auto_create_index': True,
        'index_background': True,
    }


class TaggedData(me.EmbeddedDocument):

    sentence = me.StringField(required=True)
    tag = me.StringField(required=True)


class SentenceTagged(me.Document):

    # tagged_by = me.StringField(required=True)
    jd_id = me.StringField(required=True)
    tagged_data = me.EmbeddedDocumentListField(TaggedData)

    meta = {
        'indexes': ['jd_id'],
        'auto_create_index': True,
        'index_background': True,
    }
