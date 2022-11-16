# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


class COMMON(object):
    '''
    CURRENCY     = { 'usd' : 'usd' , 'eur' : 'eur' }
    STATE        = { 'completed' : 1 , 'pending' : 2, 'refunded' : 3 }
    PAYMENT_TYPE = { 'cc' : 1 , 'paypal' : 2, 'wire' : 3 }

    USERS_ROLES  = { 'ADMIN'  :1 , 'USER'      : 2 }
    USERS_STATUS = { 'ACTIVE' :1 , 'SUSPENDED' : 2 }

    # check verified_email
    VERIFIED_EMAIL = { 'verified' :1 , 'not verified' : 2 }
    '''

    # Used by products
    CURRENCY_USD = 'usd'
    CURRENCY_EUR = 'eur'

    # Used by Products & Sales
    STATE_COMPLETED = 'completed'
    STATE_PAID = 'paid'
    STATE_PENDING = 'pending'
    STATE_REFUNDED = 'refunded'

    ROLE_ADMIN = 1
    ROLE_USER = 2

    USER_INACTIVE = 0
    USER_ACTIVE = 1
    USER_SUSPENDED = 2

    PAYMENT_CC = 'cc'
    PAYMENT_PAYPAL = 'paypal'
    PAYMENT_WIRE = 'wire'

    EMAIL_NOT_VERIFIED = 0
    EMAIL_VERIFIED = 1
