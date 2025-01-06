import os
from modules.ctd_converter import CTD_Converter

ctd = CTD_Converter("20230901_MFS_CTD1432.txt")

print(ctd.array_convertion())
