# -*- coding:utf-8  -*-

from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from com.pnfsoftware.jeb.core.units.code.android.dex import IDexAnnotationItem
import os.path as opath
import struct

class DumpDexStrings(IScript):
    def __GetOutFile(self):
        self.__script_dir = opath.dirname(opath.abspath(__file__))
        return open(opath.join(self.__script_dir, 'strings.txt'), 'wb')

    def run(self, ctx):
        self.ctx = ctx

        engctx = ctx.getEnginesContext()
        if not engctx:
            print('Back-end engines not initialized')
            return

        projects = engctx.getProjects()
        if not projects:
            print('There is no opened project')
            return

        prj = projects[0]
        out_file = self.__GetOutFile()
        units = RuntimeProjectUtil.findUnitsByType(prj, IDexUnit, False)
        for uint in units:
            ss = uint.getStrings()
            for s in ss:
                v = s.getValue().strip('\n\r\t ')
                if len(v) > 0:
                    try:
                        out_file.write(v.encode('utf-8') + b'\n')
                    except Exception,e:
                        print(e)

            out_file.write('--------------------\n')
        out_file.close()
        print('------DONE------')
