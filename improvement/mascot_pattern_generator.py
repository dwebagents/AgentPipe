#!/usr/bin/env python3
"""AgentPipe Mascot Crochet Pattern Generator"""
import argparse
B=lambda n,m,r,a:chr(10).join([chr(61)*60,'  '+n.upper()+' CROCHET PATTERN',chr(61)*60]+['  - '+x for x in m]+['']+['  R'+str(i[0])+': '+i[1] for i in r]+['']+['  - '+x for x in a]+['','  Happy crocheting!'])
p=argparse.ArgumentParser();p.add_argument('-m');a=p.parse_args();print(B('Banana','Yellow|Brown|Hook|Stuffing|Eyes'.split("|"),[(1,'MR,6sc'),(2,'incx6'),(3,'(sc,inc)x6')],['Stem']))