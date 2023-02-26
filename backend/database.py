import contextlib
import itertools
import sqlite3
from contextlib import closing
from flask import g

DATABASE = "users.db"


def init_db():
    tasks = [
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT)",
        "CREATE TABLE IF NOT EXISTS steps (id INTEGER PRIMARY KEY, user_id INTEGER, day INTEGER, value INTEGER, "
        "UNIQUE(user_id, day) ON CONFLICT REPLACE, FOREIGN KEY (user_id) REFERENCES users(id))",
        "CREATE TABLE IF NOT EXISTS anxieties (id INTEGER PRIMARY KEY, user_id INTEGER, timestamp INTEGER, value INTEGER, "
        "UNIQUE(user_id, timestamp) ON CONFLICT REPLACE, FOREIGN KEY (user_id) REFERENCES users(id))",
        "CREATE TABLE IF NOT EXISTS heartrates (id INTEGER PRIMARY KEY, user_id INTEGER, timestamp INTEGER, value INTEGER, "
        "UNIQUE(user_id, timestamp) ON CONFLICT REPLACE, FOREIGN KEY (user_id) REFERENCES users(id))",
    ]

    with closing(sqlite3.connect(DATABASE)) as db:
        execute_multiple_tasks(db, tasks, itertools.repeat((), len(tasks)))


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# INSERT
def execute_single_task_no_return(db, command, param):
    execute_multiple_tasks_no_return(db, [command], [param])


def execute_multiple_tasks_no_return(db, commands, params):
    with contextlib.closing(db.cursor()) as cursor:
        for command, param in zip(commands, params):
            cursor.execute(
                command,
                param,
            )
        db.commit()


# SELECT
def execute_single_task(db, command, param):
    return execute_multiple_tasks(db, [command], [param])[0]


def execute_multiple_tasks(db, commands, params):
    with contextlib.closing(db.cursor()) as cursor:
        return list(
            map(
                lambda command_param_pair: cursor.execute(
                    command_param_pair[0], command_param_pair[1]
                ).fetchall(),
                zip(commands, params),
            )
        )
