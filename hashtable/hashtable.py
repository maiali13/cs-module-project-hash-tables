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
        self.table = [None] * int(self.capacity)
        self.num_keys = 0 # count of keys and values
        # self.max_load_factor = 0.7
        # self.min_load_factor = 0.2


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
        Return the load factor for this hash table.
        aka all occupied space
        (number of keys / capacity)
        """
        # number_keys = sum(1 for x in filter(None.__ne__, self.table))
        return int(self.num_keys / self.capacity)


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
    
        return hash & 0xFFFFFFFF


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        aka creates index value based on the key
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        -find slot for key
        -search linked list for key
        -update list if found
        -if not found, add it to the list/ update HashTableEntry 
        """
        index = self.hash_index(key)
        head = self.table[index]
        node = HashTableEntry(key, value)

        if head is not None: 
            node = self.table[index]
            head = self.table[index].next

        else:
            node = self.table[index]
            self.num_keys += 1

        # STRETCH
        if self.get_load_factor() <= 0.2:
            # If load factor less than 0.2 (underloaded), cut size in half
            self.resize(self.capacity / 2)

        elif self.get_load_factor() >= 0.7:
            # If load factor greater than 0.7 (overloaded), double size
            self.resize(2 * self.capacity)


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        - find slot for key
        - search ll for key
        - delete from list if found + return deleted value
        - return None if not found
        """
        index = self.hash_index(key)
        head = self.table[index] # setting head node
        keyFound = False
        prev = None
        current = head
        while current is not None:
            if current.key == key:
                keyFound = True
                self.num_keys -= 1
                if prev is not None:
                    prev.next = current.next
                else:
                    head = current.next
                return
            else:
                prev = current
                current = current.next
            
        if not keyFound:
            print('Error: Key {} not found to delete'.format(key))
        else:
            print('Key {} deleted'.format(key))


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        -find slot for key
        -search ll for key
        -if not found, return none
        -if found, return value
        """
        index = self.hash_index(key)
        head = self.table[index]

        while head is not None:
            if head.key == key: #if correct, return value for the key
                return head.value
            else:   #otherwise move on
                head = head.next
        return None


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.
        aka remove everything from old hash array, put it in new resized array

        - create new array (double if larger, half if smaller)
        - O(n) traverse old hash table
        - for each element: find its slot in new array and place it there
        STRETCH: do this automatically when hashtable is overloaded or underloaded
        ht is overloaded when load factor > 0.7
        ht is underloaded when load factor < 0.2
        """
        new_ht = HashTable(new_capacity) # create new array
        
        for item in self.table:
            while item is not None:
                new_ht.put(item.key, item.value)
                item = item.next
        
        self.capacity = new_ht.capacity
        self.table = new_ht.table


    #for testing    
    def check_large(self):
        print(f"\nFactor: {ht.get_load_factor():.3f}")
        print(f"Size: {ht.capacity}, Count: {ht.num_keys}")
        print(f"Data: {ht.table}")
    def check_small(self):
        print(f"\nFactor: {ht.get_load_factor():.3f}")
        print(f"Size: {ht.capacity}, Count: {ht.num_keys}")


if __name__ == "__main__":
    ht = HashTable(8)

    #test load factor
    ht.check_large()

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.check_small()

    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.check_small()

    ht.put("line_3", "All mimsy were the borogoves,")
    ht.check_small()

    ht.put("line_4", "And the mome raths outgrabe.")
    ht.check_small()

    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.check_small()

    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.check_small()

    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.check_small()

    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.check_small()

    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.check_small()

    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.check_small()

    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.check_small()

    ht.put("line_12", "And stood awhile in thought.")
    ht.check_small()

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # factor check
    ht.check_large()

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # factor check
    ht.check_large()
    print("")

    print(ht.djb2("line_1"))
    print(ht.fnv1("line_1"))
    print(ht.hash_index("line_1"))

    print(ht.djb2("line_9"))
    print(ht.fnv1("line_9"))
    print(ht.hash_index("line_9"))

    print(ht.djb2("line_10"))
    print(ht.fnv1("line_10"))
    print(ht.hash_index("line_10"))
    print("")