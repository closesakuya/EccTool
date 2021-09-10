# -*- coding: utf-8 -*-
"""
用于生成pyd文件后再生成exe,增加反编译难度
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='any words.....',
    ext_modules=cythonize(["../AdPicEcc.py", "../main_ui.py", "../imgs.py"],
                          language_level=3
                          ),
)