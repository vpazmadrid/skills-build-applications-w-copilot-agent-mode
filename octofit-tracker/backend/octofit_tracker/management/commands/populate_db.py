from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from pymongo import ASCENDING

# Sample data
USERS = [
    {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
    {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
    {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
    {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
    {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
    {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
]

TEAMS = [
    {"name": "Marvel", "members": ["Iron Man", "Captain America", "Black Widow"]},
    {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]},
]

ACTIVITIES = [
    {"user": "Superman", "activity": "Flight", "duration": 60},
    {"user": "Iron Man", "activity": "Suit Training", "duration": 45},
    {"user": "Batman", "activity": "Martial Arts", "duration": 30},
]

LEADERBOARD = [
    {"user": "Superman", "points": 1000},
    {"user": "Iron Man", "points": 950},
    {"user": "Batman", "points": 900},
]

WORKOUTS = [
    {"name": "Strength Training", "level": "Advanced"},
    {"name": "Cardio Blast", "level": "Intermediate"},
    {"name": "Yoga Flex", "level": "Beginner"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        db = connection.cursor().db_conn
        # For Djongo, db_conn is a pymongo.database.Database instance
        # Drop and recreate collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Ensure unique index on email
        db.users.create_index([("email", ASCENDING)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
