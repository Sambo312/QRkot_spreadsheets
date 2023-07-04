def force_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


async def commit_refresh(
    object_,
    session
):
    session.add(object_)
    await session.commit()
    await session.refresh(object_)
