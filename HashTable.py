class HashTableWChains:
    def __init__(self, initial_capacity=40):
        """Initialize the hash table with a specified initial capacity."""
        self.table = [[] for _ in range(initial_capacity)]

    def insert(self, key, item):
        """Insert an item with a specific key into the hash table."""
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item  # Update existing item.
                return True
        bucket_list.append([key, item])  # Append new item if not found.
        return True

    def search(self, key):
        """Search for an item by key in the hash table and return the item if found."""
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None  # Return None if the item is not found.

    def remove(self, key):
        """Remove an item by key from the hash table if it exists."""
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
        return False  # Return False if the item was not found to be removed.