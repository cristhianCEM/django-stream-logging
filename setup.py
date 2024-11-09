from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='django-stream-logging',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=5.0.0',
        'colorlog>=5.0.0'
    ],
    setup_requires=['wheel'],
    python_requires='>=3.10',
    license='MIT',
    description='Django stream logging classes for views and commands.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cristhianCEM/django-stream-logging',
    author='cristianCEM',
    author_email='cristianbcer27@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    keywords=['Django', 'logging', 'stream', 'views', 'commands']
)
