import os, sqlite3, pyodbc
from flask import g

from app.common.databaseQueries import DatabaseQueries


class Sqlite3Database(DatabaseQueries):
    '''
    Custom database class to interface with a sqlite3 database
    Based on the sqlite3 library connection and cursor class
    Interfacing the DatabaseQueries class which wraps around the DatabaseInterface class
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
        return self.cursor().lastrowid



class MicrosoftSQLDatabase(DatabaseQueries):
    '''
    Custom database class to interface with a Microsoft SQL database
    Based on the pyodbc library connection and cursor class
    Interfacing the DatabaseQueries class which wraps around the DatabaseInterface class
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
            self._open_and_save_db_in_g()
        return g.sql_db_conn


    def _get_cursor(self):
        ''' Get the cursor object for the current application context, if it doens't exists create it '''

        if 'sql_db_cursor' not in g:
            self._open_and_save_db_in_g()
        return g.sql_db_cursor


    def _open_and_save_db_in_g(self):
        cursor, conn = self._open_database()
        g.sql_db_cursor = cursor
        g.sql_db_conn = conn

    

    def execute(self, sql, parameters=()):
        ''' Execute an sql statement with optional parameters to the current transaction '''
        self.cursor().execute(sql, parameters)
        return self.cursor()


    def commit(self):
        '''Commit the changes in the current transaction made by sql statements to the database '''
        self.cursor().commit()


    def last_row_id(self):
        ''' Get the id of the last row that was added into the database, this is only set if an INSERT statement was used '''
        return self.cursor().execute('select SCOPE_IDENTITY()').fetchone()[0]