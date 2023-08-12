def combine_dicts(*dicts: dict) -> dict:
    """Combine Dicts in one Dict"""
    if len(dicts) == 1:
        return dicts[0]
    return {**dicts[0], **combine_dicts(*dicts[1:])}
