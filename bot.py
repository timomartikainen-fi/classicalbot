import json
import logging

from musicbrainz.db import MusicBrainzDatabase
from musicbrainz.editing import MusicBrainzEditing
from wikidata.wikidata_provider import WikidataProvider

logger = logging.getLogger(__name__)

# settings from config file
with open("classicalbot.conf") as f:
    config = json.load(f)

if __name__ == '__main__':

    # converting string from config to numeric constant
    log_level_numeric = getattr(logging, config["log"]["log_level"].upper(), logging.INFO)

    # setting a logger, with settings from config
    logging.basicConfig(
        filename = config["log"]["log_file"],
        datefmt = "%Y-%m-%d %H:%M:%S",
        format = "%(asctime)s %(levelname)-8s %(message)s",
        level = log_level_numeric
    )

    logger.info("--- BOT STARTING ---")

    mb_editing = MusicBrainzEditing(config)

    #wd = WikidataProvider(config)

    #wikidata_key = wd.get_key("Q644152")
    #print(wikidata_key)

    with mb_editing as mb:

        mb_open_edit_count = mb.open_edits_count()
        print(f'Open edits: {mb_open_edit_count}')

        #mb.set_work_key('d5a6d2a2-298b-41e8-94ae-507393d775d8')


    #max_edits = config['config']['max_open_edits'] - mb_open_edit_count
    #max_daily_edits = config['config']['max_daily_edits']



    '''
    # continuing if max_open_edits set at the config file is smaller than the amount of actual open edits
    if edit_budget > 0:

        for i in range(min(max_edits, max_daily_edits)):

            print(f'Edit {i+1}')
'''
    #db = MusicBrainzDatabase(config)
    #works = db.works_without_key()
    #print(works)
    #print(f'Count of works without a key: {len(works)}')

    '''
    check db
    check api
    update via editing
    edit-work.attributes.0.type_id  1
    edit-work.attributes.0.value    11
    edit-work.edit_note             "note"

    https://test.musicbrainz.org/ws/2/work/d5a6d2a2-298b-41e8-94ae-507393d775d8?fmt=json

    '''

    logger.info("--- BOT STOPPING ---")