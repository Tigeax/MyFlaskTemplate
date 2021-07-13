

# TODO commenting reference to databaseQueries
class DatabaseInterface():
    '''
    Custom database class to wrap around a database library to interact with the database
    Using the Flask global environment to only open the database once during a request
    Multiple instances of this class can be created without issue. As only one database connection will exist per request
    Can only be used in the application context
    '''

    def __init__(self, app):
        self.app = app


    def _open_database(self):
        ''' Open the connection to the database '''
        if self.app.config['DEBUG']:
            print("DEBUG: Database opened")


    def _close_database(self, error):
        '''
        Close the database if it is open
        Called by the Flask teardown_appcontext to close the datbase at the end of the request
        '''
        if self.app.config['DEBUG']:
            print("DEBUG: Database closed")
    

    @property
    def connection(self):
        ''' Get the connection object of the connection to the database for the current application context, if it doens't exists create it '''
        pass


    @property
    def cursor(self):
        ''' Get the cursor object for the current application context, if it doens't exists create it '''
        pass


    def execute(self, sql: str, parameters: tuple) -> None:
        ''' Execute an sql statement with optional parameters to the current transaction '''

        sql = "".join(sql.splitlines()) # Convert to a single line string
        sql = sql.replace("  ", "") # Remove extra spaces

        if self.app.config['DEBUG']:
            print(f"DEBUG: Database execute, '{sql}', {parameters}")


    def commit(self) -> None:
        '''Commit the changes in the current transaction made by sql statements to the database '''
        if self.app.config['DEBUG']:
            print("DEBUG: Database commit")


    def last_row_id(self) -> int:
        ''' Get the id of the last row that was added into the database, this is only set if an INSERT statement was used '''
        pass