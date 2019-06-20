import mongoengine

from common.conf import config
from common.utils.externals import to_dict

from errors import ServiceException
from models import JobDescription, SentenceTagged, TaggedData


RESULTS_PER_PAGE = config.get('RESULTS_PER_PAGE')


class JobDescriptionService(object):

    def _validate_jd(self, jd):
        try:
            jd.validate()
            return jd
        except mongoengine.ValidationError:
            return None
    
    def save_job_descriptions(self, job_descriptions):
        """
        saves multiple job descriptions at a time

        job_descriptions - type -> list of dicts
                         - {'jd_id', 'jd_title', jd_html', 'jd_sentences'}
        """

        if not job_descriptions:
            raise ServiceException('job descriptions are required')

        jd_insts = [JobDescription(**{
            'jd_id': jd.get('jd_id'),
            'jd_title': jd.get('jd_title'),
            'jd_html': jd.get('jd_html'),
            'jd_sentences': jd.get('jd_sentences')
        }) for jd in job_descriptions]

        validated_jds = list(filter(
            lambda x: x is not None, map(self._validate_jd, jd_insts)
        ))
        
        if validated_jds:
            JobDescription.objects.insert(validated_jds)

        return {'inserted_docs': len(validated_jds)}

    def get_jd_ids_based_on_status(self, tagged=False):
        """
        returns a list of all job description ids based on tagging
        status
        """

        tagged_jd_ids = list(map(
            lambda x: x.jd_id, SentenceTagged.objects.all().only('jd_id')
        ))

        untagged_jds = JobDescription.objects.filter(jd_id__nin=tagged_jd_ids)\
            .only('jd_id')

        return [jd.jd_id for jd in untagged_jds] if not tagged else \
            tagged_jd_ids

    def get_job_descriptions_for_page(self, page_number, tagged=False):
        """
        get job descriptions for a given page number
        """

        skip = (page_number - 1) * RESULTS_PER_PAGE
        limit = RESULTS_PER_PAGE

        jd_ids = self.get_jd_ids_based_on_status(tagged=tagged)
        all_jds = JobDescription.objects.filter(jd_id__in=jd_ids)

        filtered_jds = all_jds.skip(skip).limit(limit)

        return [{'jd_title': jd.jd_title, 'jd_id': jd.jd_id} for jd in filtered_jds], \
            all_jds.count()

    def get_job_descriptions_for_search(self, title, page_number, tagged=False):
        """
        get job descriptions for search
        """

        skip = (page_number - 1) * RESULTS_PER_PAGE
        limit = RESULTS_PER_PAGE

        jd_ids = self.get_jd_ids_based_on_status(tagged=tagged)
        jds_search = JobDescription.objects(
            jd_id__in=jd_ids, jd_title={'$regex': fr'(?i){title}'}
        )
        jds_search_paginate = jds_search.skip(skip).limit(limit)

        return [{'jd_title': jd.jd_title, 'jd_id': jd.jd_id} for jd in jds_search_paginate], \
            jds_search.count()

    def get_jd_details(self, jd_id):
        """
        returns the list of sentences and html for a given jd id
        """

        jd = JobDescription.objects.filter(jd_id=jd_id).first()

        if not jd:
            raise ServiceException('no jd with id {}'.format(jd_id))
        
        return to_dict(jd)


class SentenceTaggedService(object):

    def perform_sentence_tagging(self, jd_id, tags):
        """
        performs sentence tagging for a given job description
        """

        tagged_data = [
            TaggedData(**{
                'sentence': tag.get('sentence'),
                'tag': tag.get('tag')
            }) for tag in tags
        ]

        SentenceTagged.objects.filter(jd_id=jd_id)\
            .modify(upsert=True, set__tagged_data=tagged_data)

        return {'tagged': True}
                                
    def get_tagged_sentences_for_jd(self, jd_id):
        """
        returns the data for all the tagged sentences along with
        tags for a given job description
        """

        st = SentenceTagged.objects.filter(jd_id=jd_id).first()

        if not st:
            return {'taggings': []}

        return {'taggings': list(map(to_dict, st.tagged_data))}
