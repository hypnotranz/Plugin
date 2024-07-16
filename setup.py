from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Connect to MongoDB (without authentication)
client = MongoClient('localhost', 27017)

# Create admin user (if not exists)
admin_db = client['admin']
try:
    admin_db.command("createUser", "admin", pwd="adminPassword", roles=["userAdminAnyDatabase"])
    print("Admin user created.")
except DuplicateKeyError:
    print("Admin user already exists.")

# Reconnect with admin credentials
client = MongoClient('localhost', 27017, username='admin', password='adminPassword', authSource='admin')

# Create or switch to the "plugin" database
plugin_db = client['plugin']

# Create a user with administrative privileges on the "plugin" database
try:
    plugin_db.command("createUser", "pluginUser", pwd="pluginPassword", roles=["dbOwner"])
    print("User 'pluginUser' created with administrative privileges on the 'plugin' database.")
except DuplicateKeyError:
    print("User 'pluginUser' already exists. Updating roles...")
    plugin_db.command("grantRolesToUser", "pluginUser", roles=[{"role": "dbOwner", "db": "plugin"}])
    print("Roles updated for 'pluginUser'.")

print("Done.")
