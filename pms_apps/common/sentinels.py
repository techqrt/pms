class _NotProvided:
    """Marks a field as absent from the request, distinct from an explicit null/clear value."""

    def __repr__(self):
        return "NOT_PROVIDED"

    def __bool__(self):
        return False


NOT_PROVIDED = _NotProvided()
