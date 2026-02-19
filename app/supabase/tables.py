from flask import current_app
from postgrest import SyncRequestBuilder, SyncSelectRequestBuilder

from app.supabase.columns import Column
from app.supabase.helpers import cols


class Table:
    """
    Base class for Supabase table definitions.

    Example usage:
        class User(Table):
            TABLE_NAME = "user"

            EMAIL = Column("email")
            NAME = Column("name")
            CREATED_AT = Column("created_at", datetime_column)

        # Query examples:
        User.query().select("*").execute()
        User.select_by_id(cols(User.EMAIL, User.NAME), 1).execute()
    """

    TABLE_NAME = ""
    ID = Column("id")

    @classmethod
    def query(cls) -> SyncRequestBuilder:
        return current_app.supabase_client.table(cls.TABLE_NAME)

    @classmethod
    def join(cls, *columns: str):
        """Build a join query string for related tables."""
        return f"{cls.TABLE_NAME}({cols(*columns)})"

    @classmethod
    def select_by_id(cls, columns: str, id: int) -> SyncSelectRequestBuilder:
        return cls.query().select(columns).eq(cls.ID, id).maybe_single()

    @classmethod
    def unwrap(cls, data: dict):
        """Extract nested table data from a join query result."""
        return data[cls.TABLE_NAME]

    @classmethod
    def find_by_id(cls, data: list[dict], id: str):
        """Find a row by ID in a list of rows."""
        for row in data:
            if cls.ID(row) == id:
                return row

        return None


# Example table definition (uncomment and modify as needed):
#
# class User(Table):
#     TABLE_NAME = "user"
#
#     CLERK_ID = Column("clerk_id")
#     EMAIL = Column("email")
#     NAME = Column("name")
#     CREATED_AT = Column("created_at", datetime_column)
