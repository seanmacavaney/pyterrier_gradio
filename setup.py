from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='pyterrier_gradio',
    version='0.0.1',
    description='Tools for building PyTerrier demos using Gradio',
    url='https://github.com/seanmacavaney/pyterrier_gradio',
    classifiers=[
    ],
    packages=['pyterrier_gradio'],
    # as per splade
    long_description=readme,
    install_requires=[
        'python-terrier', 'gradio'
    ],
    package_data={
        'pyterrier_gradio': ['pyterrier_gradio/style.css'],
    },
)
