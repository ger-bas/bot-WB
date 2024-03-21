import asyncio


def check_subscribe(tack_name: str) -> object | None:
    """Checks whether a task with a specific name exists."""
    tasks = [t for t in asyncio.all_tasks() if t.get_name() == tack_name]
    if tasks:
        return tasks[0]
    return


def find_vendor_code(text: str) -> str:
    """Search for "vendor_code" in the message."""
    sub_str = 'Артикул:   '
    index1 = text.find(sub_str, 0) + len(sub_str)
    index2 = text.find('\n', index1, index1 + 22)

    return text[index1:index2]
