__all__ = ['test_func_1', 'test_func_2', 'srv_get_stock_list_from_sse', 'srv_init_table_stock_list_to_mysql', 'srv_load_stock_data_from_em']

def test_func_1():
    pass

def test_func_2():
    pass

import sys
if "/home/fred/dev/Quantum/" not in sys.path:
    sys.path.append("/home/fred/dev/Quantum/")
from data_engine.data_interface.stock_data_if import srv_get_stock_list_from_sse, srv_init_table_stock_list_to_mysql, srv_load_stock_data_from_em