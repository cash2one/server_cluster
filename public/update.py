#coding:utf-8
'''
    Jan.Lonely Yan
    Sun Jul 19 09:47:40 2015
'''
import sys
import types
import gc

class CReloadModule(object):
    def __init__(self, module_name):
        self.m_module_name = module_name

    def Process(self):
        cur_module = sys.modules.get(self.m_module_name)
        if not cur_module:
            return
        update_dicts = dict(cur_module.__dict__)

        reload(cur_module)
        gc.collect()

        function_set = set()
        class_set = set()
        for _key, _value in update_dicts.items():
            if isinstance(_value, types.FunctionType):
                function_set.add(_key)
            elif self.IsClass(_value):
                class_set.add(_key)
                self.ProcessClasses(_value, getattr(cur_module, _value.__name__))
            else:
                self.ProcessGlobalData(cur_module, _key, _value)
        self.CommonLoginfo(pylog.INFO, "Process", "function:%s, class:%s" %(function_set, class_set))
        return True

    def CommonLoginfo(self, log_level, fucntion_name, addinfo):
        pylog.Log(log_level, "%s %s %s module_name:%s" %(self.__class__.__name__, fucntion_name, addinfo, self.m_module_name))

    def IsClass(self, _value):
        return isinstance(_value, types.ClassType) or hasattr(_value, '__bases__')

    def ProcessClasses(self, _value_old, _value_new):
        objs = gc.get_referents(_value_old)
        for cur_object in objs:
            if isinstance(cur_object, list):
                for index, item in enumerate(cur_object):
                    if item == _value_old:
                        cur_object[index] = _value_new

            elif isinstance(cur_object, dict):
                obj_copy = cur_object.copy()
                for _key, _value in obj_copy.iteritems():
                    # _key 和 _value 是同一类型有BUG
                    if _key == _value_old:
                        if _value != _value_old:
                            cur_object[_value_new] = cur_object[_key]
                        else:
                            cur_object[_value_new] = _value_new
                        del cur_object[_key]
                    elif _value == _value_old:
                        cur_object[_key] = _value_new

            elif isinstance(cur_object, _value_old):
                cur_object.__class__ = _value_new

            elif self.IsClass(cur_object):
                if issubclass(cur_object, _value_old):
                    if len(cur_object.__bases__) == 1:
                        cur_object.__bases__ = (_value_new, )

    def ProcessGlobalData(self, module, _key, _value):
        if _key.isupper():
            return
        if isinstance(_value, types.ModuleType):
            return
        setattr(module, _key, _value)


def ReloadModuleByModuleName(module_name):
    reload_process = CReloadModule(module_name)
    reload_process.Process()

if __name__ == "__main__":
    ReloadModuleByModuleName("pylog")
