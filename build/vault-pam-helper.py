# -*- coding: utf-8 -*-
#

import syslog
import traceback
import requests

DEFAULT_USER  = "nobody"
DEBUGGING = True

def logging(facility, message):
    if (facility != syslog.LOG_DEBUG) or DEBUGGING:
        syslog.openlog(facility=facility)
        syslog.syslog(facility, message)
        syslog.closelog()


def get_config(argv):
    """
    Read the parameters from the arguments. If the argument can be split with a
    "=", the parameter will get the given value.
    :param argv:
    :return: dictionary with the parameters
    """
    config = {}
    for arg in argv:
        argument = arg.split("=")
        if len(argument) == 1:
            config[argument[0]] = True
        elif len(argument) == 2:
            config[argument[0]] = argument[1]
    return config

def pam_sm_authenticate(pamh, flags, argv):

    config = get_config(argv)
    
    global DEBUGGING
    DEBUGGING = (config.get("debug", None) != None)

    logging(syslog.LOG_DEBUG, "Starting PAM authentication...{}".format(config))

    prompt = config.get("prompt", "Vault Password")
    if prompt[-1] != ":":
        prompt += ":"

    url = "{}/v1/auth/userpass/login/{}".format(
        config.get("vault_addr", "http://localhost:8200"),
        pamh.get_user(None) or DEFAULT_USER
    )

    sslverify = not config.get("nosslverify", False)
    cacerts = config.get("cacerts")
    if sslverify and cacerts:
        sslverify = cacerts
    
    logging(syslog.LOG_DEBUG, "URL: {}".format(url))

    rval = pamh.PAM_AUTH_ERR

    try:
        if pamh.authtok is None:
            message = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "%s " % prompt)
            response = pamh.conversation(message)
            pamh.authtok = response.resp

        payload = {"password": pamh.authtok}
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, json=payload, headers=headers, verify=sslverify)

        logging(syslog.LOG_DEBUG, response.text)

        if (response.status_code == 200):
            rval = pamh.PAM_SUCCESS

    except Exception as e:
        logging(syslog.LOG_ERR, traceback.format_exc())
        logging(syslog.LOG_ERR, "%s: %s" % (__name__, e))

    except requests.exceptions.SSLError:
        logging(syslog.LOG_CRIT, "%s: SSL Validation error. Get a valid "
                                 "SSL certificate, For testing you can use the "
                                 "options 'nosslverify'." % __name__)

    return rval

def pam_sm_setcred(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
  return pamh.PAM_SUCCESS
