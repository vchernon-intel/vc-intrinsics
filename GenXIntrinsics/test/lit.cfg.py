#=========================== begin_copyright_notice ============================
#
# Copyright (C) 2020-2021 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice (including the next
# paragraph) shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT
#============================ end_copyright_notice =============================

# -*- Python -*-

import lit.formats
import lit.util

from lit.llvm import llvm_config
from lit.llvm.subst import ToolSubst
from lit.llvm.subst import FindTool

# Configuration file for the 'lit' test runner.

# name: The name of this test suite.
config.name = 'vc-intrinsics'

# testFormat: The test format to use to interpret tests.
config.test_format = lit.formats.ShTest(not llvm_config.use_lit_shell)

# suffixes: A list of file extensions to treat as test files.
config.suffixes = ['.ll']

# excludes: A list of directories  and files to exclude from the testsuite.
config.excludes = ['CMakeLists.txt', 'Plugin']

used_llvm = "llvm{}".format(config.llvm_version_major)
config.available_features = [used_llvm]

# test_source_root: The root path where tests are located.
config.test_source_root = os.path.dirname(__file__)

# test_exec_root: The root path where tests should be run.
config.test_exec_root = os.path.join(config.test_run_dir, 'test_output')

llvm_config.use_default_substitutions()

config.substitutions.append(('%PATH%', config.environment['PATH']))

tool_dirs = [config.llvm_tools_dir]

# Add extra args for opt to remove boilerplate from tests.
opt_extra_args = ['-load', config.vc_intrinsics_plugin]

# Add option for new pass manager plugins. Extension instead of
# replacement is needed to hack option parsing mechanism. Argument of
# '-load' is processed during initial option parsing and all passes
# from plugin are registed in legacy PM. This registration allows to
# add passes to new PM via command line options in the same way as
# with old PM. Otherwise, -passes=<pass> option will be used for new PM and
# -<pass> for old PM. Additionally, LLVM will load plugin only once
# because it permanently loads libraries with caching behavior.
if int(config.llvm_version_major) >= 13:
    opt_extra_args.extend(['-load-pass-plugin', config.vc_intrinsics_plugin])

tools = [ToolSubst('opt', extra_args=opt_extra_args)]

llvm_config.add_tool_substitutions(tools, tool_dirs)
