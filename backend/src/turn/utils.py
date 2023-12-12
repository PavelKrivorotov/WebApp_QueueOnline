from secrets import token_hex


def make_queue_key() -> str:
    return token_hex(32)
