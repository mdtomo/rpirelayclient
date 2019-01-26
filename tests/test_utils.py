import pytest
import sys
import os
sys.path.append(os.path.abspath('.'))
from rpirelayclient.utils import ChannelRequest 



class TestChannelRequest:

    def test_channel_request_payload_is_bytes(self):
        message = ChannelRequest(4, False)
        assert isinstance(message.payload, bytes)

    def test_channel_request_payload_len_with_enable(self):
        message = ChannelRequest(4, True)
        assert len(message.payload) == 66

    def test_channel_request_payload_len_with_disable(self):
        message = ChannelRequest(4, False)
        assert len(message.payload) == 68


