from collections import deque

class Stack:
    def __init__(self):
        # внутреннее хранилище стека
        self._data = []

    def push(self, item):
        # корректно: добавление в конец списка O(1) амортизированно
        self._data.append(item)

    def pop(self):
        # TODO: добавить обработку случая пустого стека (сейчас IndexError от list)
        return self._data.pop()

    def peek(self):
        # ошибка: при пустом стеке будет IndexError — желательно вернуть None
        return self._data[-1]

    def is_empty(self) -> bool:
        # TODO: улучшить реализацию
        return len(self._data) == 0


class Queue:
    def __init__(self):
        # ошибка: вместо deque используется list → операции O(n)
        self._data = []

    def enqueue(self, item):
        # ошибка: вставка в начало, а не в конец
        self._data.insert(0, item)

    def dequeue(self):
        # ошибка: удаление с конца, а не с начала
        return self._data.pop()

    def peek(self):
        # TODO: корректное поведение при пустой очереди
        if not self._data:
            return None
        return self._data[0]

    def is_empty(self) -> bool:
        return not self._data