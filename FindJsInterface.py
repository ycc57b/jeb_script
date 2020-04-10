# -*- coding:utf-8  -*-

from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from com.pnfsoftware.jeb.core.units.code.android.dex import IDexAnnotationItem

class FindImp:
    def __init__(self, uint):
        self.__uint = uint

    def __GetAnnotationName(self, annotation):
        index = annotation.getTypeIndex()
        value_type = self.__uint.getType(index)
        return value_type.getName()

    def __IsJsInterfaceAnnotation(self, method_annotation):
        annotation_items = method_annotation.getAnnotationItemSet()
        for annotation_item in annotation_items:
            if annotation_item.getVisibility() != IDexAnnotationItem.VISIBILITY_RUNTIME:
                    continue
            annotation = annotation_item.getAnnotation()
            if self.__GetAnnotationName(annotation) == 'JavascriptInterface':
                return True
        return False

    def __AnnotationToMethod(self, annotation):
        method_index = annotation.getMethodIndex()
        print(self.__uint.getMethod(method_index).getAddress())

    def FindJsInterface(self, clz):
        annotation_dir = clz.getAnnotationsDirectory()
        if not annotation_dir:
            return
        method_annotations = annotation_dir.getMethodsAnnotations()
        for method_annotation in method_annotations:
            if self.__IsJsInterfaceAnnotation(method_annotation):
                self.__AnnotationToMethod(method_annotation)

class FindJsInterface(IScript):
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
        units = RuntimeProjectUtil.findUnitsByType(prj, IDexUnit, False)
        for uint in units:
            imp = FindImp(uint)
            clzes = uint.getClasses()
            for clz in clzes:
                imp.FindJsInterface(clz)
