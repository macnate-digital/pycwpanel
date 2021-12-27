import functools
import requests
import validators

from dynaconf import settings
from urllib.parse import urljoin

# CWP ERROR MESSAGES
CWP_ERR_MUST_INDICATE_USER = 'must indicate a user'
CWP_ERR_USER_DOESNOT_EXIST = 'User does not exist'
CWP_ERR_ACCOUNT_DOESNOT_EXIST = 'Account does not exist'
CWP_ERR_MUST_INDICATE_EMAIL = 'You must indicate an email'
CWP_ERR_NO_PACKAGE_FOUND = 'There is no package with this name'
CWP_ERR_UPDATE_ERROR = 'There was an error updating'
CWP_ERR_USER_IS_ROOT = 'User is root'

CWP_ERROR_MESSAGES = [
    CWP_ERR_MUST_INDICATE_USER,
    CWP_ERR_ACCOUNT_DOESNOT_EXIST,
    CWP_ERR_USER_DOESNOT_EXIST,
    CWP_ERR_MUST_INDICATE_EMAIL,
    CWP_ERR_NO_PACKAGE_FOUND,
    CWP_ERR_UPDATE_ERROR,
    CWP_ERR_USER_IS_ROOT
]

# CWP API URL
CWP_API_URL = settings.CWP_API_URL
CWP_API_URL = urljoin(CWP_API_URL, "v1")
CWP_API_KEY = settings.CWP_API_KEY

# The CWP API does not support HTTP (including localhost), therefore
# any request is redirected to HTTPS with a self-signed certificate
# on the CWP server.
# If the supplied CWP API URL is not a public url i.e. the host is
# either `localhost` or a private IP e.g. 192.168.1.22, we
# have to set verify to False on every request to the API to avoid
# SSL check errors.
cwp_url_is_public = validators.url(CWP_API_URL, public=True)
VERIFY_SSL_ON_REQUESTS = True if cwp_url_is_public else False


def api_request(func: object) -> object:
    """
    This function acts as a decorator for custom functions
    that use the Python requests library.

    It helps in automatically adding the CWP API key as the
    first parameter to any custom request function,
    then allows the other params to be added as well.
    """

    default_params = {
        'key': CWP_API_KEY
    }

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # set up all the request params
        params = {}
        params.update(default_params)
        params.update(kwargs)

        # run the request func with the params
        func(*args, **params)
        return func(*args, **params)

    return wrapper


class CWPApiRequest(object):
    """
    This is an abstract class for custom HTTP
    request functions for the CWP API.

    The custom request functions extend the Python requests library functions,
    and they use the custom api_request decorator to automatically add the
    CWP API key as the first param in any request, then supplied
    kwargs are also added to the request.

    Any subclass of this will require an invocation_function (the CWP makers
    call it that so we'll keep it that way) which defines the endpoint where
    the request will hit.

    For example, to get account details of a user account on CWP, we'll need
    to hit the /accountdetail endpoint of the CWP API. The URL is constructed
    in this abstract class with the provided invocation function.

    The URL in this case will be - https://localhost:2304/v1/accountdetail
    """

    invocation_function = None

    def __init__(self):

        self.cwp_request_url = urljoin(
            CWP_API_URL, self.invocation_function)

    @api_request
    def post(self, **kwargs):
        return requests.post(
            self.cwp_request_url, data={**kwargs},
            verify=VERIFY_SSL_ON_REQUESTS)

    @api_request
    def put(self, **kwargs):
        return requests.put(
            self.cwp_request_url, data={**kwargs},
            verify=VERIFY_SSL_ON_REQUESTS)

    @api_request
    def patch(self, **kwargs):
        return requests.patch(
            self.cwp_request_url, data={**kwargs},
            verify=VERIFY_SSL_ON_REQUESTS)

    @api_request
    def delete(self, **kwargs):
        return requests.delete(
            self.cwp_request_url, data={**kwargs},
            verify=VERIFY_SSL_ON_REQUESTS)


class CWPAccountApiRequest(CWPApiRequest):
    """
    This subclass hits the /account endpoint which deals
    with one or many user accounts

    A sample successful response from the CWP API /account?action=list query
    which returns all user accounts with their details looks like this:

    {   "status":"OK",
        "msj":
            [
                {
                    "package_name":"Starter",
                    "idpackage":"2",
                    "id":"1",
                    "backup":"on",
                    "username":"macnated",
                    "email":"info@macnate.digital",
                    "setup_date":"2021-06-22 18:07:33",
                    "ip_address":"192.168.10.122",
                    "domain":"macnate.digital",
                    "reseller":"",
                    "owner":"root",
                    "diskused":0,"
                    "disklimit":"5000","
                    "bandwidth":"",
                    "bwlimit":"100000",
                    "status":"suspended"
                    },

                {
                    <another dict>
                }
            ]
    }
    """

    invocation_function = "/account"

    def add_user(self, **kwargs):
        self.post(action='add', **kwargs)

    def get_users(self):
        return self.post(action='list')

    def update_user(self, **kwargs):
        return self.post(action='udp', **kwargs)

    def delete_user(self, **kwargs):
        return self.post(action='del', **kwargs)

    def suspend_user(self, username):
        return self.post(action='susp', user=username)

    def unsuspend_user(self, username):
        return self.post(action='unsp', user=username)

    def get_usernames(self):
        data = self.get_users().json()['msj']

        return [d.get('username') for d in data]
