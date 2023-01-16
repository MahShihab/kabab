def decode_flask_cookie(secret_key, cookie_str):
    import hashlib
    from itsdangerous import URLSafeTimedSerializer
    from flask.sessions import TaggedJSONSerializer
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.loads(cookie_str)


print(decode_flask_cookie('kfhsjhfaflk', 'eyJfZnJlc2giOmZhbHNlLCJfdXNlcl9pZCI6IjEifQ.Y8UkMQ.V9UG0NkCWhulgLTz3farsq8YaaE'))