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


print(decode_flask_cookie('futdyrgf kbjihoutdyrjxfhcgvkbihotr75stxgfh jkoi', '1|a961260834bc1e858c5627e71347218f5d80bd7680591f5057582bf49ff27db47aebee2ac06f4e91df9fbcaefeedf658560829232466398140ed1f650336d573'))