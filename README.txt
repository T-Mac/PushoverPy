PushoverPy
===========
PushoverPy provides a simple api to pushover.net, and a command line client. Sending messages is as easy as::

    from PushoverPy import Pushover
    
    Api = Pushover(User_Key, Api_Token)
    Api.send('Hello World')

Or from the comand line::

    pushoverpy --usey-key <user_key> --token <api_token> --message "Hello World"
	
Development is hosted on `Github <https://github.com/T-Mac/PushoverPy/blob/master/Pushover.py>`_.