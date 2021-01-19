#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import io
import os
import tarfile
from subprocess import check_output, CalledProcessError

import sys
from setuptools import setup, find_packages, Command

bootstrap_dependencies = [
    'pip==20.0.2',
    'setuptools==46.1.3',
    'wheel==0.34.2',
]


def parse_requirements(resolve_version=True, add_bootstrap_dependencies=False):
    def transform_editable(d):
        if resolve_version:
            if d.startswith('-e'):
                return d[2:].strip().split('/')[-1] + '==' + version
            else:
                return d
        else:
            return d

    with open(os.path.join(dir_setup, 'requirements.txt')) as f:
        dependencies = [transform_editable(x.strip()) for x in f.readlines()]

    if add_bootstrap_dependencies:
        dependencies = dependencies + bootstrap_dependencies

    return dependencies


def exec_command(command, show_output=False):
    try:
        stdout = check_output(command)
        if show_output:
            print(stdout.decode('utf-8'))
        return stdout
    except CalledProcessError as e:
        print(e.output.decode('utf-8'))
        raise


def download_dependencies():
    os.makedirs('build/dep_wheels', exist_ok=True)
    exec_command(['pip', 'wheel', '--wheel-dir=%s' % 'build/dep_wheels', '-r', 'requirements.txt'], show_output=True)
    exec_command(['pip', 'wheel', '--wheel-dir=%s' % 'build/dep_wheels'] + bootstrap_dependencies, show_output=True)


def make_deployable_tgz():
    def reset(tarinfo):
        print(tarinfo.name)
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = "root"
        if ('/bin/' in tarinfo.name or '/service/' in tarinfo.name) and tarinfo.isreg():
            # Make scripts executable
            tarinfo.mode = 0o0755
        return tarinfo

    def project_files(tarinfo):
        if '__pycache__' in tarinfo.name:
            return None

        files_to_include = [
            'config',
            'ek_optical',
            'ek_optical_test',
            'migrations',
            'spec',
            '.env',
            'app.py',
            'manage.py',
            # 'requirements.txt',
            'setup.py',
        ]

        if tarinfo.name.endswith('/common/app'):
            tarinfo.uid = tarinfo.gid = 0
            tarinfo.uname = tarinfo.gname = "root"
            return tarinfo

        for file_to_include in files_to_include:
            if tarinfo.name.endswith('/common/app/' + file_to_include) or f'/common/app/{file_to_include}/' in tarinfo.name:
                tarinfo.uid = tarinfo.gid = 0
                tarinfo.uname = tarinfo.gname = "root"
                return tarinfo

        return None

    dist_base = os.path.join(dir_setup, 'build', 'dist')
    dist_tgz = os.path.join(dist_base, 'optical-dist-{}.tgz'.format(version))
    os.makedirs(dist_base, exist_ok=True)
    dist_folder = 'optical-dist-' + version
    with tarfile.open(dist_tgz, 'w:gz') as deployed:
        deployed.add('package', dist_folder, filter=reset)
        deployed.add('build/dep_wheels', dist_folder + '/env/common/wheels/dep')

        deployed.add('.', dist_folder + '/env/common/app', filter=project_files)
        deployed.add('webapp/dist', dist_folder + '/env/common/webapp-dist')

        requirements = tarfile.TarInfo(dist_folder + '/env/common/app/requirements.txt')
        requirements.uid = requirements.gid = 0
        requirements.uname = requirements.gname = "root"
        data = '\n'.join(parse_requirements(resolve_version=True, add_bootstrap_dependencies=True)).encode()
        requirements.size = len(data)
        deployed.addfile(requirements, io.BytesIO(data))


class PackageCommand(Command):
    description = "make a deployable tgz"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        download_dependencies()
        make_deployable_tgz()


def check_python_version():
    if sys.version_info[:2] < (3, 5):
        print('Python 3.5 or newer is required. Python version detected: {}'.format(sys.version_info))
        sys.exit(-1)


def main():
    with open('README.rst') as readme_file:
        readme = readme_file.read()

    setup_requirements = ['pytest-runner', ]
    test_requirements = ['pytest>=3', ]

    setup(
        author="Ekitech",
        author_email='info@ekitech.cn',
        license='Ekitech Proprietary',
        python_requires='>=3.5',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        description='ek_disco, commit: {0}'.format(commit),
        entry_points={
            'console_scripts': [
                'ek_optical=manage:run_main',
            ],
        },
        install_requires=parse_requirements(),
        long_description=readme,
        include_package_data=True,
        keywords='ek_optical',
        name='ek_optical',
        packages=find_packages(include=['ek_optical', 'ek_optical.*', ]),
        cmdclass={'package': PackageCommand},
        setup_requires=setup_requirements,
        test_suite='ek_optical_tests',
        tests_require=test_requirements,
        url='http://gitlab.lab.ekitech.ai/',
        version=version,
        zip_safe=False,
    )


if __name__ == '__main__':
    dir_setup = os.path.dirname(os.path.realpath(__file__))
    version = os.environ['BUILD_NUMBER'] if 'TEAMCITY_VERSION' in os.environ else '0+workingcopy'
    commit = os.environ['BUILD_VCS_NUMBER'] if 'TEAMCITY_VERSION' in os.environ else 'workingcopy'

    check_python_version()
    main()
