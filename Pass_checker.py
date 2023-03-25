import requests
import hashlib
import sys

# calling api request fundction.
def api_request(hash_char):
    url = 'https://api.pwnedpasswords.com/range/' + hash_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Response error: {res.status_code} chack API')
    return res.text


def pass_check(tail,response,password):
    full_hash = [line.split(":") for line in response.splitlines()]
    for h, count in full_hash:
        if tail in h:
            c = count
            print(f"'{password}' found in {c} times, try to change it")
            return 0
    print(f"'{password}' not found, carry on!")


def passwd(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pass[:5],sha1pass[5:]
    response = api_request(first5_char)
    pass_check(tail,response,password)

    
def main(args):
    for arg in args:
        passwd(arg)
    return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


