from src.utils import gen_uuid, upload_image
import uuid


def is_valid_gen_uuid(uuid_val):
    try:
        uuid.UUID(str(uuid_val))
        return True
    except ValueError:
        return False


#  test if the generated uuid is a valid uuid
def test_is_valid_uuid():
    valid_uuid = gen_uuid()
    assert is_valid_gen_uuid(valid_uuid) == True


# TODO: test file (images, video) uplaods to cloudinary
