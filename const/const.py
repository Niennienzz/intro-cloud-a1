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
    # images
    ORIGIN = 'origin.jpg'
    THUMB = 'thumbnail.jpg'
    TRANS_1 = 'trans1.jpg'
    TRANS_2 = 'trans2.jpg'
    TRANS_3 = 'trans3.jpg'

    # hash
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # aws
    MANAGER_DATABASE_ID = 1
    USER_WORKER_IMAGE_ID = 'ami-fa6cd180'
    SECURITY_GROUP = 'ECE-1779'
    KEY_NAME = 'ece1779_p1'
    ELB_NAME = 'ECE-1779-LoadBalancer'
