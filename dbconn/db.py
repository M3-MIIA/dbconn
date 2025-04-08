from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from .get_secrets import get_secret

def connect_to_db(tenant_id='public'):
    DB_URL = get_secret()
    dbschema=tenant_id
    DB: AsyncEngine = create_async_engine(DB_URL,
        connect_args={'options': '-csearch_path={}'.format(dbschema)})

    return DB