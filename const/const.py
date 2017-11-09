class Constants:
    """Constants provides access to useful constants.

        Attributes:
            ORIGIN (str): The filename of the original image.
            THUMB (str): The filename of the thumbnail image.
            TRANS_1 (str): The filename of the 1st transformation.
            TRANS_2 (str): The filename of the 2nd transformation.
            TRANS_3 (str): The filename of the 3rd transformation.
            ALPHABET (str): The alphabet including 1-9, a-z, and A-Z for salt generation.
            INSTANCES (slice of str): Pre-loaded instance IDs.
    """
    ORIGIN = 'origin.jpg'
    THUMB = 'thumbnail.jpg'
    TRANS_1 = 'trans1.jpg'
    TRANS_2 = 'trans2.jpg'
    TRANS_3 = 'trans3.jpg'
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    INSTANCES = [
        'i-0b1a939ffe9f95e49',
        'i-0f9f4f730b4dd6010',
        'i-04191223ea538d254',
        'i-04b911a38a48d8802',
        'i-0855f8345171caf50',
        'i-0a11bc36d70c8ae84',
        'i-0cceb5164e35b555a',
        'i-0f26719f10f7820b1'
    ]
