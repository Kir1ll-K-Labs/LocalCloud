class SendingEvent:
    def __init__(self,addresses:[str],event_data=None,event_name:str=""):
        self.addresses=addresses
        self.event_name=event_name
        self.event_data=event_data