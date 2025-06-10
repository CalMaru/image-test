from enum import Enum, auto


class StrEnum(str, Enum):
    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value.lower() == other.lower()
        return super().__eq__(other)

    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class LogLevel(StrEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
