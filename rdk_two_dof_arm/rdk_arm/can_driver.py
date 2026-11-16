"""Vendor-specific interface placeholder. No invented CAN protocol."""


class CANDriver:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "Real CAN driver not implemented: supply motor protocol, IDs, "
            "units, feedback decoding, enable/disable and timeout behavior first."
        )
