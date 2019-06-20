from .views import tagger


api_urls = [
    ('/jd', tagger.jd, ['GET'], 'get all the jds per page'),
    ('/sent/<jd_id>',tagger.sent,['GET','POST'],'tagging page')
]
