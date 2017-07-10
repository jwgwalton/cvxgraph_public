from setuptools import setup

setup(
    name='cvxgraph',
    version='0.0.1',
    author='Joseph Walton',
    author_email='jwgwalton@gmail.com',
    packages=['cvxgraph',
              'cvxgraph.constraints',
              'cvxgraph.graphs',
              'cvxgraph.utils'],
    package_dir={'cvxgraph': 'cvxgraph'},
    url='',
    license='Apache v2.0',
    zip_safe=False,
    description='Implementation of graph algorithms using CVXPY',
    install_requires=[],
    use_2to3=True,
)



