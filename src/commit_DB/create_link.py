def execute_insert(insert_stmt: str, connection):
    cursor = connection.cursor()
    cursor.execute(insert_stmt)
    connection.commit()


def link_headline_place(headline_id: int, place_id: int, connection):
    insert_stmt = f"INSERT INTO HeadlinePlaces(headlineId, placeId) values({headline_id}, {place_id})"
    execute_insert(insert_stmt)


def link_headline_person(headline_id: int, person_id: int, connection):
    insert_stmt = f"INSERT INTO HeadlinePlaces(headlineId, person_id) values({headline_id}, {person_id})"
    execute_insert(insert_stmt, connection)


def link_headline_org(headline_id: int, org_id: int, connection):
    insert_stmt = f"INSERT INTO HeadlinePlaces(headlineId, person_id) values({headline_id}, {org_id})"
    execute_insert(insert_stmt, connection)






