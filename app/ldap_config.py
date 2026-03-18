import ldap
from flask import current_app

def ldap_authenticate(email, password):
    try:
        conn = ldap.initialize(f"ldap://{current_app.config['LDAP_HOST']}")
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)

        base_dn = current_app.config['LDAP_BASE_DN']
        filter_str = f"(mail={email})"
        result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, filter_str, ['dn'])
        if not result:
            return None
        user_dn = result[0][0]

        conn.simple_bind_s(user_dn, password)
        conn.unbind_s()

        username = user_dn.split(',')[0].split('=')[1]
        return {'username': username}
    except ldap.INVALID_CREDENTIALS:
        return None
    except Exception:
        return None