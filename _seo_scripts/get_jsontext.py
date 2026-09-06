# -*- coding: utf-8 -*-
import re, sys
fn = sys.argv[1]
s = open(fn, encoding="utf-8").read()
for m in re.finditer(r'"text":"([^"]{0,500})"', s):
    print("JSONTEXT>>>", m.group(1))
    print("---")
