from controls import ChannelSwitch

message_queue = []

def toggle_channel(number):
    ChannelSwitch.instances[number].status = not ChannelSwitch.instances[number].status
    message_queue.append((number, ChannelSwitch.instances[number].status))


# class Payload():

#     def __init__(self, length, ):