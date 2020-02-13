"""
   Copyright 2013, Shinya Takamaeda-Yamazaki and Contributors

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   ----
   Verilog Preprocessor
 
   Icarus Verilog is used as the internal preprocessor.
   Please install Icarus Verilog on your environment.
"""

from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import subprocess
from wheezy.template.engine import Engine
from wheezy.template.ext.code import CodeExtension
from wheezy.template.ext.core import CoreExtension
from wheezy.template.ext.vpp  import VPPAdapterExtension
from wheezy.template.loader import FileLoader

try:
    import json
except ImportError:  # pragma: nocover
    try:
        import simplejson as json
    except ImportError:  # pragma: nocover
        json = None

def load_context(sources):
    c = {}
    for s in sources:
        if s.endswith('.json'):
            s = json.load(open(s))
        else:
            s = json.loads(s)
        c.update(s)
    return c

class VerilogPreprocessor(object):
    def __init__(self, filelist, outputfile='pp.out', include=None, define=None):

        if not isinstance(filelist, (tuple, list)):
            filelist = list(filelist)
            
        self.filename = filelist
        if isinstance(filelist, list) or isinstance(filelist, tuple):
            self.filename = filelist[0]
        self.searchpath =['.']
        self.context = load_context(define)
        
        if not include is None:
            for i in include:
                self.searchpath.append(i)

    def preprocess(self):
        ts = '`'
        extensions = [CoreExtension(ts), CodeExtension(ts), VPPAdapterExtension(ts, ts)]
        engine = Engine(FileLoader(self.searchpath), extensions)
    #     engine.global_vars.update({'h': escape})
        t = engine.get_template(self.filename)
        return t.render(self.context)


def preprocess(
    filelist,
    output='preprocess.output',
    include=None,
    define=None
):
    pre = VerilogPreprocessor(filelist, output, include, define)
    return pre.preprocess()