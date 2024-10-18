from setuptools import setup, find_packages


requirements = [
    'python-docx',
]

setup(
    name='deal_excel_and_json',
    version='0.1.2',
    python_requires='>=3.8',
    author='zhoujing GXKJ',
    author_email='zhoujing@gx.com',
    url='https://perfectbullet.github.io/',
    description='demo of setup.py',
    license='MIT-0',
    packages=find_packages('.'),
    zip_safe=True,
    install_requires=requirements,
)
