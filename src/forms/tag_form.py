# from flask_wtf import FlaskForm
from wtforms import Form, SelectField, StringField, FieldList, FormField, TextAreaField
from choices import TAG_CHOICES


class SentenceTag(Form):
    sentence = TextAreaField('sentence')
    tag = SelectField('tags', choices=[(c, c) for c in TAG_CHOICES])


class TagEntryForm(Form):
    tag_list = FieldList(FormField(SentenceTag))
