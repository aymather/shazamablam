from etc.ClientBase import ClientBase
from etc.settings import db_string


# Database Client (Controller to postgres db)
class DbClient(ClientBase):

    def __init__(self):
        ClientBase.__init__(self, db_string)

    def search_artists(self, searchText):

        string = """
            select *
            from shazamablam.artists
            where name ~* :searchText
        """
        params = { 'searchText': searchText }
        return self.execute(string, params)
