class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        # ошибка: размер не обновляется
        self._size = 0

    def append(self, value):
        """Добавить элемент в конец списка"""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            # TODO: добавить увеличение размера
            return

        # неэффективность: полный обход списка O(n)
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
        # TODO: self._size += 1

    def prepend(self, value):
        """Добавить элемент в начало списка"""
        new_node = Node(value, next=self.head)
        self.head = new_node
        # TODO: обновить размер

    def insert(self, idx, value):
        """Вставка по индексу — неполная реализация, есть ошибки"""
        if idx < 0:
            raise IndexError("negative index is not supported")

        if idx == 0:
            self.prepend(value)
            return

        current = self.head
        # ошибка: нет проверки выхода за границы
        for _ in range(idx - 1):
            current = current.next

        new_node = Node(value, next=current.next)
        current.next = new_node
        # TODO: увеличить размер

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __len__(self):
        # ошибка: всегда возвращает 0
        return self._size

    def __repr__(self):
        values = list(self)
        return f"SinglyLinkedList({values})"