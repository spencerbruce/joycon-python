import hid
from .constants import JOYCON_VENDOR_ID, JOYCON_PRODUCT_IDS
from .constants import JOYCON_L_PRODUCT_ID, JOYCON_R_PRODUCT_ID, JOYCON_PRO_PRODUCT_ID


def get_device_ids(debug=False):
    """
    returns a list of tuples like `(vendor_id, product_id, serial_number)`
    """
    devices = hid.enumerate(0, 0)

    out = []
    for device in devices:
        vendor_id      = device["vendor_id"]
        product_id     = device["product_id"]
        product_string = device["product_string"]
        serial = device.get('serial') or device.get("serial_number")

        if vendor_id != JOYCON_VENDOR_ID:
            continue
        if product_id not in JOYCON_PRODUCT_IDS:
            continue
        if not product_string:
            continue

        out.append((vendor_id, product_id, serial))

        if debug:
            print(product_string)
            print(f"\tvendor_id  is {vendor_id!r}")
            print(f"\tproduct_id is {product_id!r}")
            print(f"\tserial     is {serial!r}")

    return out


def is_id_L(id):
    return id[1] == JOYCON_L_PRODUCT_ID


def get_ids_of_type(lr, **kw):
    """
    returns a list of tuples like `(vendor_id, product_id, serial_number)`

    arg: lr : str : put `R` or `L` or `PRO`
    """
    if lr.lower() == "l":
        product_id = JOYCON_L_PRODUCT_ID
    elif lr.lower() == 'r':
        product_id = JOYCON_R_PRODUCT_ID
    else: # pro controller
        product_id = JOYCON_PRO_PRODUCT_ID
    return [i for i in get_device_ids(**kw) if i[1] == product_id]


def get_R_ids(**kw):
    """returns a list of tuple like `(vendor_id, product_id, serial_number)`"""
    return get_ids_of_type("R", **kw)

def get_L_ids(**kw):
    """returns a list of tuple like `(vendor_id, product_id, serial_number)`"""
    return get_ids_of_type("L", **kw)

def get_PRO_ids(**kw):
    """returns a list of tuple like `(vendor_id, product_id, serial_number)`"""
    return get_ids_of_type("PRO", **kw)

def get_R_id(**kw):
    """returns a tuple like `(vendor_id, product_id, serial_number)`"""
    ids = get_R_ids(**kw)
    if not ids:
        raise ConnectionError("Failed to connect to right joycon. Ensure it is powered on and paired and try again.")
    return ids[0]

def get_L_id(**kw):
    """returns a tuple like `(vendor_id, product_id, serial_number)`"""
    ids = get_L_ids(**kw)
    if not ids:
        raise ConnectionError("Failed to connect to left joycon. Ensure it is powered on and paired and try again.")
    return ids[0]

def get_PRO_id(**kw):
    """returns a tuple like `(vendor_id, product_id, serial_number)`"""
    ids = get_PRO_ids(**kw)
    if not ids:
        raise ConnectionError("Failed to connect to pro controller. Ensure it is powered on and paired and try again.")
    return ids[0]