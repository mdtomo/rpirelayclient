from controls import ChannelSwitch
import json


message_queue = []


# TODO
# CommandRequest - Baseclass
# ChannelRequest - Subclass
# SystemRequest - Subclass
# LoggingRequest - Subclass
# CommandResponse - Baseclass

# class CommandRequest():

#     @property

#     def __init__(self, data):
#         # isinstance checking
#         self.data = data
#         self._fixed_header = len(data).to_bytes(2, byteorder='big')


class ChannelRequest():
    
    def __init__(self, channel_number, state):
        self.channel_number = channel_number
        self.state = state

    @staticmethod
    def _create_message_header_payload(message_type, message_length):
        message_header = { 
            'message_type': message_type,
            'message_length': message_length
        }
        return json.dumps(message_header).encode()
        
    @staticmethod
    def _create_message_payload(channel_number, state):
        return json.dumps((channel_number, state)).encode()

    @property
    def payload(self):
        message_bytes = self._create_message_payload(self.channel_number, self.state)
        message_header_bytes = self._create_message_header_payload(self.__class__.__name__, len(message_bytes))
        fixed_header_bytes = len(message_header_bytes).to_bytes(2, byteorder='big')
        return fixed_header_bytes + message_header_bytes + message_bytes


def toggle_channel(number):
    ChannelSwitch.instances[number].status = not ChannelSwitch.instances[number].status
    #message_queue.append((number, ChannelSwitch.instances[number].status))
    channel_request = ChannelRequest(number, ChannelSwitch.instances[number].status)
    message_queue.append(channel_request.payload)