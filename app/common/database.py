import os, sqlite3, pyodbc
from flask import g


class DatabaseInterface():
    '''
    Custom database class to wrap around a database library to interact with the database.
    Using the Flask global environment to only open the database once during a request
    '''

    def __init__(self):
        pass

    def _open_database(self):
        pass

    def _close_database(self, error):
        pass

    def _get_connection(self):
        pass

    def _get_cursor(self):
        pass

    def execute(self, sql: str, parameters: tuple) -> None:
        pass

    def commit(self) -> None:
        pass

    def last_row_id(self) -> int:
        pass




class Sqlite3Database(DatabaseInterface):
    '''
    Custom database class to interface with a sqlite3 database
    Based on the sqlite3 library connection and cursor class
    Using the Flask global environment to only open the database once during a request
    '''

    def __init__(self, dbPath=os.getenv("SQLITE3_DATABASE_PATH")):
        self.dbPath = dbPath

    
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


    def _get_connection(self):
        return self._get_cursor().connection


    def _get_cursor(self):
        ''' Get the cursor object for the current application context, if it doens't exists create it '''

        if 'sqlite3_db_cursor' not in g:
            cursor = self._open_database()
            g.sqlite3_db_cursor = cursor
        return g.sqlite3_db_cursor
    

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



class MicrosoftSQLDatabase():
    '''
    Custom database class to interface with a Microsoft SQL database
    Based on the pyodbc library connection and cursor class
    Using the Flask global environment to only open the database once during a request
    '''

    def __init__(self, server=os.getenv("SQL_SERVER"), database=os.getenv("SQL_DATABASE"), username=os.getenv("SQL_SERVER_USERNAME"), password=os.getenv("SQL_SERVER_PASSWORD")):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    
    def _open_database(self):
        '''
        Open the connection to the SQL databse
        Return a cursor object of the connection
        '''
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
        cursor = conn.cursor()
        print("DEBUG: Database opened")
        return cursor, conn


    def _close_database(self, error):
        '''
        Close the database if it is open
        Called by the Flask teardown_appcontext to close the datbase at the end of the request
        '''
        SQLDbCursor = g.pop('sql_db_cursor', None)
        SQLDbConn = g.pop('sql_db_conn', None)

        if SQLDbConn is not None:
            print("DEBUG: Database closed")
            SQLDbConn.close()

    def _get_connection(self):
        ''' Get the connection object for the current application context, if it doens't exists create it '''

        if 'sql_db_conn' not in g:
            cursor, conn = self._open_database()
            g.sql_db_cursor = cursor
            g.sql_db_conn = conn
        return g.sql_db_conn


    def _get_cursor(self):
        ''' Get the cursor object for the current application context, if it doens't exists create it '''

        if 'sql_db_cursor' not in g:
            cursor, conn = self._open_database()
            g.sql_db_cursor = cursor
            g.sql_db_conn = conn
        return g.sql_db_cursor

    

    def execute(self, sql, parameters=()):
        ''' Execute an sql statement with optional parameters to the current transaction '''
        self.cursor().execute(sql, parameters)
        return self.cursor()


    def commit(self):
        '''Commit the changes in the current transaction made by sql statements to the database '''
        self.cursor().commit()


    def last_row_id(self):
        ''' Get the id of the last row that was added into the database, this is only set if an INSERT statement was used '''
        lastRowId = self.cursor().execute('select SCOPE_IDENTITY()').fetchone()[0]
        return lastRowId