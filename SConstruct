import os
import shutil

AddOption(
        '--naconfig',
        dest='naconfig',
        type='string',
        action='store',
        default='default.naconfig',
        help='configuration file location')
config = GetOption('naconfig')
if not config.endswith('.naconfig'):
    config += '.naconfig'
shutil.copyfile(config, 'build/current.naconfig')

env = Environment()

SOURCE_DIR = 'src'
Export('SOURCE_DIR')

env.SConscript('sources.scons')
env.SConscript(
        'generate_sources.scons',
        variant_dir='derived_src', src_dir=SOURCE_DIR,
        duplicate=0)
env.SConscript(
        'compile.scons',
        variant_dir='build', src_dir='derived_src',
        duplicate=0)
compile_vpi = env.SConscript('vpi_pyeval/SConstruct')

Import('compiled_tests')
Depends(compiled_tests, compile_vpi)

# vim:ft=python:
