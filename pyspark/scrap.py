from typing import Optional

def find_node(node: Optional[ListNode], value: int) -> Optional[ListNode]:
    if node is None:
        return None
    if node.value == value:
        return node
    return find_node(node.next, value)