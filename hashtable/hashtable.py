class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __repr__(self):
        return (f"(key = {self.key}, value = {self.value})")

# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys
    Implement this.
    """

    def __init__(self, capacity=MIN_CAPACITY):
        self.capacity = capacity
        self.data = [None] * capacity
        self.count = 0

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)
        One of the tests relies on this.
        Implement this.
        """
        return self.capacity

    def get_load_factor(self):
        """
        Returns (total / self.capacity) aka all occupied space
        """
        return (self.count / self.capacity)

    def update_load_factor(self):
        """
        Recalculate the load factor
        Added for stretch implementation
        """
        self.load_factor = (self.count / self.capacity)

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function

        Implement this, and/or DJB2.
        """
        total = 0
        for n in key.encode():
            total += n
            total &= 0xffffffffffffffff #64 bit
        
        return total


    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        Implement this, and/or FNV-1.
        """
        hash = 5381
        for x in key:
            hash = (hash * 33) + ord(x)
        return hash

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.
        Hash collisions should be handled with Linked List Chaining.
        """
        # Use hash_index to create index value based on the key
        index = self.hash_index(key)

        if self.data[index] is None:
            # No collision. New key so insert value
            self.data[index] = HashTableEntry(key, value)
            self.count += 1

        else:
            # Collision!
            node = self.data[index]

            while node.key != key and node.next is not None:
                node = node.next

            if node.key == key:
                # Duplicate key -> update value
                node.value = value
            else:
                # New key -> insert value
                node.next = HashTableEntry(key, value)
                self.count += 1

        # STRETCH
        self.update_load_factor()
        if self.load_factor > 0.7:
            self.resize()

    def delete(self, key):
        """
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        Implement this.
        """
        index = self.hash_index(key)

        if self.data[index] is None:
            # If no matching hash, nothing to delete
            print("Error: Key not found.")
            return None

        else:
            node = self.data[index]
            prev = None
            while node.key != key and node.next is not None:
                prev = node
                node = node.next

            if node.key == key:
                # Key found -> delete
                if prev is None:
                    self.data[index] = node.next
                else:
                    prev.next = node.next

                # STRETCH
                # check load factor, re-size if necessary
                self.count -= 1
                self.update_load_factor()
                if self.load_factor < 0.2 and self.capacity >= 16:
                    self.resize(self.capacity // 2)
                return node.value

            else:
                print("Error: Key not found.")
                return None
        

    def get(self, key):
        """
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        Implement this.
        """
        index = self.hash_index(key)
        if self.data[index] is None:
            # Not found, return none
            return None
        else:
            node = self.data[index]
            while node.key != key and node.next is not None:
                node = node.next
            if node.key == key:
                # Found -> return value
                return node.value
            else:
                # Not found
                return None

    def resize(self, new_capacity= None):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.
        aka remove everything from old hash array, put it in new resized array

        - create new array (double if larger, half if smaller)
        - O(n) traverse old hash table
        - for each element: find its slot in new array and place it there

        STRETCH: 
        do this automatically when hashtable is overloaded or underloaded
        ht is overloaded when load factor > 0.7
        ht is underloaded when load factor < 0.2
        """
        old_data = self.data

        if new_capacity is None:
            new_capacity = len(self.data) * 2

        self.data = [None] * new_capacity
        self.capacity = new_capacity

        for node in old_data:
            while node is not None:
                self.put(node.key, node.value)
                self.count -= 1
                node = node.next

        self.update_load_factor()
   
    def check_ht(self):
        """
        for testing
        """
        print(f"\nFactor: {ht.get_load_factor():.3f}")
        print(f"Size: {ht.capacity}, Count: {ht.count}")
        # print(f"Data: {ht.data}")

if __name__ == "__main__":
    ht = HashTable(8)

    # Factor check
    ht.check_ht()

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Factor check
    ht.check_ht()

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Factor check
    ht.check_ht()
    print("")

    print("\nLine 1")
    print(ht.djb2("line_1"))
    print(ht.fnv1("line_1"))
    print(ht.hash_index("line_1"))
    
    print("\nLine 3")
    print(ht.djb2("line_3"))
    print(ht.fnv1("line_3"))
    print(ht.hash_index("line_3"))

    print("\nLine 6")
    print(ht.djb2("line_6"))
    print(ht.fnv1("line_6"))
    print(ht.hash_index("line_6"))

    print("\nLine 9")
    print(ht.djb2("line_9"))
    print(ht.fnv1("line_9"))
    print(ht.hash_index("line_9"))

    print("\nLine 12")
    print(ht.djb2("line_12"))
    print(ht.fnv1("line_12"))
    print(ht.hash_index("line_12"))
    print("")