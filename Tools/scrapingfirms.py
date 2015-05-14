__author__ = 'Maxime'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from lxml import html
import urllib2


def main():
    pass

if __name__ == '__main__':
    main()


def getfirms():
    page = urllib2.urlopen("http://www.societes-cotees.fr/societes-cotees.php")

    tree = html.fromstring(str(page.read().decode('latin-1')))

    firmisin = tree.xpath('//table/tr[@class="odd"]/td[1]/text() | //table/tr[@class="even"]/td[1]/text()')
    firmcode = tree.xpath('//table/tr[@class="odd"]/td[2]/text() | //table/tr[@class="even"]/td[2]/text()')
    firmname = tree.xpath('//table/tr[@class="odd"]/td[3]/a/text() | //table/tr[@class="even"]/a/td[3]/text()')

    result = []

    for isin,  code, name in zip(firmisin, firmcode, firmname):
        result.append({'FirmISIN': isin, 'FirmCode': code, 'FirmName': name})



    return result


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    char = []
    for c in range(ord(c1), ord(c2)+1):
        char.append(chr(c))
    return char

print getfirms()