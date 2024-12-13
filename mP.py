class MemoryBlock:
    def __init__(self, size, address=None):
        self.size = size
        self.address = address

class MemoryAllocator:
    def __init__(self):
        self.quick_lists = {20: [], 40: [], 60: []}  
        self.general_memory_pool = []

    def allocate(self, requested_size):
        if requested_size in self.quick_lists and self.quick_lists[requested_size]:
            block = self.quick_lists[requested_size].pop(0)
            print(f"Allocated {block.size} bytes from Quick List.")
            return block
        else:
            block = self._find_suitable_block(requested_size)
            if block:
                if block.size >= requested_size:
                    remaining_size = block.size - requested_size
                    print(f"Allocated {requested_size} bytes, splitting block of {block.size} bytes.")
                    if remaining_size in self.quick_lists:
                        self.quick_lists[remaining_size].append(MemoryBlock(remaining_size, block.address))
                    return block
                else:
                    print(f"Allocated {block.size} bytes from General Memory Pool.")
                    return block
            else:
                print("Memory Allocation Failed")
                return None

    def release(self, block):
       
        if block.size in self.quick_lists:
            self.quick_lists[block.size].append(block)
            print(f"Block of size {block.size} bytes returned to Quick List.")
        else:
            self.general_memory_pool.append(block)
            print(f"Block of size {block.size} bytes returned to General Memory Pool.")

    def _find_suitable_block(self, requested_size):
        for block in self.general_memory_pool:
            if block.size >= requested_size:
                self.general_memory_pool.remove(block)
                return block
        return None



allocator = MemoryAllocator()


allocator.quick_lists[20].append(MemoryBlock(20, "QuickListBlock1"))
allocator.quick_lists[40].append(MemoryBlock(40, "QuickListBlock2"))
allocator.quick_lists[60].append(MemoryBlock(60, "QuickListBlock3"))


allocator.general_memory_pool = [
    MemoryBlock(50, "Block1"),
    MemoryBlock(65, "Block2")
]


print("Requesting 20 bytes:")
block1 = allocator.allocate(20)

print("\nRequesting 45 bytes:")
block2 = allocator.allocate(45)


print("\nReleasing block of size 20 bytes:")
allocator.release(block1)


print("\nRequesting 80 bytes:")
block5 = allocator.allocate(80)


print("\nReleasing block of size 45 bytes:")
allocator.release(block2)

