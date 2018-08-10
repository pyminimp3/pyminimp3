from setuptools import setup
from setuptools.extension import Extension

from Cython.Build import cythonize


extensions = [
    Extension(
        "pyminimp3._backend",
        sources=["lib/*.pyx"],
        language="c",
        include_dirs=[
            "lib",
             "minimp3"
        ],
    )
]


setup(
    package_dir={"": "src"},
    ext_modules=cythonize(extensions),
)
