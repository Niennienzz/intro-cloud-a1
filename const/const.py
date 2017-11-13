class Constants:
    """Constants provides access to useful constants.
    """
    # Constants for image files.
    ORIGIN = 'origin.jpg'
    THUMB = 'thumbnail.jpg'
    TRANS_1 = 'trans1.jpg'
    TRANS_2 = 'trans2.jpg'
    TRANS_3 = 'trans3.jpg'

    # Constant for SHA-256 hash salt.
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Constants for AWS related services.
    MANAGER_DATABASE_ID = 1
    USER_WORKER_IMAGE_ID = 'ami-a86ed4d2'
    SECURITY_GROUP = 'ECE-1779'
    KEY_NAME = 'ece1779_p1'
    ELB_NAME = 'ECE-1779-LoadBalancer'
