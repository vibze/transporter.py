# -*- coding: utf-8 -*-
import csv


class CSV:
    def __init__(self):
        pass

    def dump(self, array, filepath, recode=True, decoder='iso8859_5', file_properties='wb'):
        file = open(filepath, file_properties)

        d = csv.excel_tab
        d.quoting = csv.QUOTE_MINIMAL
        d.escapechar = '\\'

        writer = csv.writer(file, dialect=d)
        for row in array:
            r = []
            for s in row:
                if isinstance(s, str):
                    ss = s.replace('\t', '').replace('\n', '').replace('\\', '')
                    if recode:
                        r.append(ss.decode(decoder).encode('utf8'))
                    else:
                        r.append(ss)
                elif s == None:
                    r.append('NULL')
                elif isinstance(s, unicode):
                    r.append(s.encode('utf8'))
                else:
                    # if type(s) == str:
                    #     r.append(s.encode('utf8'))
                    # else:
                    r.append(s)
            try:
                writer.writerow(r)
            except Exception, e:
                print '-Error: %s\n%s'%(r, e)
        file.close()
        return filepath
