from enum import IntEnum

from dataclasses import dataclass


class TicketStatus(IntEnum):
    NOT_CREATED = 0
    PROCCESS_WRITING = 1
    WRITTEN = 2
    ACCEPTED = 3
    SEND_FEEDBACK = 4


@dataclass
class User:
    ticket_status: TicketStatus

