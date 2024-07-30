def chk(head):
    temp  =set()
    current = head
    while current and current.next:
        if(current in temp):
            return True
        temp.add(current)
        current=current.next
        return False
