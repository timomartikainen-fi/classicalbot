import json
import logging

import utils.constants as constants
from db import DatabaseManager

from musicbrainz.editing import MusicBrainzEditing
from wikidata.wikidata_provider import WikidataProvider

logger = logging.getLogger(__name__)

# settings from config file
with open("classicalbot.conf") as f:
    config = json.load(f)

# lists works having a key on the title but no attribute set for it
# and aren't part of another work or aren't arrangements
def works_without_key():

    # space is included to prevent "d major" matching with "mid major" or "end major"
    # work titles don't typically start with a key so this shouldn't be a major problem
    search_keys = [f"% {key}%" for key in constants.MUSICAL_KEYS_EN]

    with DatabaseManager(config['database_mb']) as db:

        query = """
            SELECT w.gid, w.name
            FROM work w
            WHERE w.name ILIKE ANY (%s)

              -- 1. no key attribute
              AND NOT EXISTS (
                  SELECT 1
                  FROM work_attribute wa
                  JOIN work_attribute_type wat ON wa.work_attribute_type = wat.id
                  WHERE wa.work = w.id
                    AND wat.gid = '7526c19d-3be4-3420-b6cc-9fb6e49fa1a9' -- key
              )

              -- 2. not a work part/movement or an arrangement
              AND NOT EXISTS (
                  SELECT 1
                  FROM l_work_work lww
                  JOIN link l ON lww.link = l.id
                  JOIN link_type lt ON l.link_type = lt.id
                  WHERE lww.entity1 = w.id
                    AND (lt.gid = 'ca8d3642-ce5f-49f8-91f2-125d72524e6a'    -- part
                        OR lt.gid = '51975ed8-bbfa-486b-9f28-5947f4370299') -- arrangement
              )
        """

        return db.execute_query(query, [search_keys])

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

    wd = WikidataProvider(config)

    wikidata_key = wd.get_key("Q644152")
    print(wikidata_key)


    '''
    with mb_editing as mb:

        mb_open_edit_count = mb.open_edits_count()
        print(f'Open edits: {mb_open_edit_count}')

        mb.set_work_key('d5a6d2a2-298b-41e8-94ae-507393d775d8')
    '''


    #max_edits = config['config']['max_open_edits'] - mb_open_edit_count
    #max_daily_edits = config['config']['max_daily_edits']



    '''
    # continuing if max_open_edits set at the config file is smaller than the amount of actual open edits
    if edit_budget > 0:

        for i in range(min(max_edits, max_daily_edits)):

            print(f'Edit {i+1}')
'''
    #works = works_without_key()
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