from setuptools import setup, find_packages
import deal_excel_and_json

requirements = [

]

setup(
    name='deal_excel_and_json',
    version=deal_excel_and_json.__version__,
    python_requires='>=3.8',
    author='zhoujing GXKJ',
    author_email='zhoujing@gx.com',
    url='https://perfectbullet.github.io/',
    description='deal_excel_and_json',
    license='MIT-0',
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements,
)
