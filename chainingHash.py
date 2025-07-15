# Custom Hash Table using chaining for collision handling
class ChainingHashTable:
    """
    A custom hash table implementation using chaining to handle collisions.
    The table is initialized with a default capacity and can store key-value pairs.
    """

    def __init__(self, capacity=40):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # A. Develop a hash table insertion function
    def insert(self, key, item):
        """
        Inserts a new item into the hash table.
        Time Complexity: O(N) in the worst case, O(1) on average.
        """
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # B. Develop a look-up function
    def search(self, key):
        """
        Searches for an item in the hash table by its key.
        Time Complexity: O(N) in the worst case, O(1) on average.
        """
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    def remove(self, key):
        """Removes an item from the hash table by its key."""
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

