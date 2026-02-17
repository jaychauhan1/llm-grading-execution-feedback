import importlib.util
import traceback

def load_func(path: str, func_name: str):
    spec = importlib.util.spec_from_file_location("student", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return getattr(mod, func_name)

def safe_call(func, args):
    try:
        out = func(*args)
        return {"ok": True, "output": out, "error": None}
    except Exception:
        return {"ok": False, "output": None, "error": traceback.format_exc()}

