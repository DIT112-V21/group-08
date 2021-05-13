class KeyBoardException(Exception):
    __module__ = "Exception thrown: Shift or Ctrl held while controlling car."
    pass


class VoiceRecognitionException(Exception):
    __module__ = "Exception thrown: Voice recognition error."
    pass


class SoundDeviceException(Exception):
    __module__ = "Exception thrown: Sound device error"
    pass
