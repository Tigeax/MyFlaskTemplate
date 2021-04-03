import os, sqlite3
from flask import g




class Sqlite3Database():
    '''
    Custom database class to interface with a sqlite3 database
    Based on the sqlite3 library connection and cursor class
    Using the Flask global environment to only open the database once during a request
    '''

    def __init__(self):
        self.dbPath = os.getenv("SQLITE3_DATABASE_PATH")

    
    def _open_database(self):
        '''
        Open the connection to the sqlite3 datbase
        Set the row factory to be a Row class to format the result of a sql request as a tuple
        Return a cursor object of the connection
        '''
        conn = sqlite3.connect(self.dbPath)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        print("DEBUG: Database opened")
        return cursor


    def _close_database(self, error):
        '''
        Close the database if it is open
        Called by the Flask teardown_appcontext to close the datbase at the end of the request
        '''
        sqlite3DbCursor = g.pop('sqlite3_db_cursor', None)

        if sqlite3DbCursor is not None:
            print("DEBUG: Database closed")
            sqlite3DbCursor.connection.close()


    def cursor(self):
        ''' Get the cursor object for the current application context, if it doens't exists create it '''

        if 'sqlite3_db_cursor' not in g:
            cursor = self._open_database()
            g.sqlite3_db_cursor = cursor
        return g.sqlite3_db_cursor


    def connection(self):
        return self.cursor().connection
    

    def execute(self, sql, parameters=()):
        ''' Execute an sql statement with optional parameters to the current transaction '''
        self.cursor().execute(sql, parameters)
        return self.cursor()


    def commit(self):
        '''Commit the changes in the current transaction made by sql statements to the database '''
        self.connection().commit()


    def last_row_id(self):
        ''' Get the id of the last row that was added into the database, this is only set if an INSERT statement was used '''
        lastRowId = self.cursor().lastrowid
        return lastRowId