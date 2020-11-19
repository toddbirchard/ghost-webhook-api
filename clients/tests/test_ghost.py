from clients import ghost


def test_get_ghost_post():
    post = ghost.get_post("5dc42cb812c9ce0d63f5bf92")
    assert post is not None
    assert post["id"] == "5dc42cb812c9ce0d63f5bf92"
