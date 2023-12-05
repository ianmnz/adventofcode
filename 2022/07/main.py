# Advent of Code : Day 07 - No Space Left On Device
# https://adventofcode.com/2022/day/7


from typing import Dict, Optional


class File:
    def __init__(self, name: str, size: int) -> None:
        self._name: str = name
        self._size: int = size

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size


class Dir:
    def __init__(self, name: str, parent: Optional['Dir'] = None) -> None:
        self._name: str = name
        self._parent = parent
        self._childs: Dict[str, Dir] = dict()
        self._files: Dict[str, File] = dict()

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Optional['Dir']:
        return self._parent

    @property
    def childs(self) -> Dict[str, 'Dir']:
        return self._childs

    def has_child(self, child_name: str) -> bool:
        return child_name in self._childs

    def child(self, child_name: str) -> 'Dir':
        return self._childs[child_name]

    def add_child(self, child_name: str) -> 'Dir':
        child = Dir(child_name, self)
        self._childs[child_name] = child
        return child

    @property
    def files(self) -> Dict[str, File]:
        return self._files

    def add_file(self, file_name: str, file_size: int) -> File:
        file = File(file_name, file_size)
        self._files[file_name] = file
        return file

    @property
    def size(self) -> int:
        size = 0
        for file in self._files.values():
            size += file.size

        for dir in self._childs.values():
            size += dir.size

        return size


def main():
    n = 100000
    sum_dir_total_size_leq_n = 0

    total_disk_space = 70000000
    needed_space = 30000000

    outermost_dir = Dir('/')
    dirs = [outermost_dir]
    dirs_sizes = dict()

    with open('input.txt', 'r') as file:
        for line in file:
            line = line.split()

            if line[0] == '$': # Command
                if line[1] == 'cd': # Cd
                    if line[2] == '/':
                        current_dir = outermost_dir

                    elif line[2] == '..':
                        current_dir = current_dir.parent
                    else:
                        if current_dir.has_child(line[2]):
                            current_dir = current_dir.child(line[2])
                        else:
                            print(f"Error : {current_dir.name} does not have child {line[2]}")

                elif line[1] == 'ls':
                    continue

            else: # Listing
                if line[0] == 'dir':
                    child = current_dir.add_child(line[1])
                    dirs.append(child)

                elif line[0].isnumeric():
                    current_dir.add_file(line[1], int(line[0]))

    # --- Part 1 --- #
    for dir in dirs:
        dir_size = dir.size
        dirs_sizes[dir.name] = dir_size
        if dir_size < n:
            sum_dir_total_size_leq_n += dir_size

    # Answer part 1 :
    print(f'Sum of total sizes of at most {n}: {sum_dir_total_size_leq_n}') # 1454188


    # --- Part 2 --- #
    total_used_space = dirs_sizes[outermost_dir.name]
    total_unused_space = total_disk_space - total_used_space
    space_to_be_freed = needed_space - total_unused_space

    if space_to_be_freed > 0:
        print(f'Needed space: {space_to_be_freed}')

        smallest_dir_to_be_deleted_name = outermost_dir.name
        smallest_dir_to_be_deleted_size = total_used_space

        for dir_name, dir_size in dirs_sizes.items():
            if dir_size > space_to_be_freed:
                if dir_size < smallest_dir_to_be_deleted_size:
                    smallest_dir_to_be_deleted_name = dir_name
                    smallest_dir_to_be_deleted_size = dir_size

        # Answer part 2 :
        print(f'Directory to be deleted: {smallest_dir_to_be_deleted_name}') # wvq
        print(f'Total size of directory to be deleted: {smallest_dir_to_be_deleted_size}') # 4183246

if __name__ == "__main__":
    main()