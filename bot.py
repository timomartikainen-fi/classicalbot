import json
import logging

from db import DatabaseManager

logger = logging.getLogger(__name__)

# settings from config file
with open("classicalbot.conf") as f:
    config = json.load(f)


# lists works having a key on the title but no attribute set for it
# and aren't part of another work or aren't arrangements
def works_without_key():

    keys = ["c-flat major", "c-flat minor", "c major", "c minor", "c-sharp major", "c-sharp minor",
        "d-flat major", "d-flat minor", "d major", "d minor", "d-sharp major", "d-sharp minor",
        "e-flat major", "e-flat minor", "e major", "e minor", "e-sharp major", "e-sharp minor",
        "f-flat major", "f-flat minor", "f major", "f minor", "f-sharp major", "f-sharp minor",
        "g-flat major", "g-flat minor", "g major", "g minor", "g-sharp major", "g-sharp minor",
        "a-flat major", "a-flat minor", "a major", "a minor", "a-sharp major", "a-sharp minor",
        "b-flat major", "b-flat minor", "b major", "b minor", "b-sharp major", "b-sharp minor"
    ]

    # space is included to prevent "d major" matching with "mid major" or "end major"
    # work titles don't typically start with a key so this shouldn't be a major problem
    search_keys = [f"% {key}%" for key in keys]

    with DatabaseManager(config['database_mb']) as db:

        query = """
            SELECT w.gid, w.name
            FROM work w
            WHERE w.name ILIKE ANY (%s)

              -- 1. no key attribute
              AND NOT EXISTS (
                  SELECT 1
                  FROM work_attribute wa
                  JOIN work_attribute_type waty ON wa.work_attribute_type = waty.id
                  WHERE wa.work = w.id
                    AND waty.gid = '7526c19d-3be4-3420-b6cc-9fb6e49fa1a9' -- key
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

    # setting a logger, with settings from config
    logging.basicConfig(
        filename = config["log"]["log_file"],
        datefmt = "%Y-%m-%d %H:%M:%S",
        format = "%(asctime)s %(levelname)-8s %(message)s",
        level = config["log"]["log_level"])

    logger.info("--- BOT STARTING ---")

    works = works_without_key()

    print(f'Count of works without a key: {len(works)}')

    logger.info("--- BOT STOPPING ---")