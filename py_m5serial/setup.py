from setuptools import setup

package_name = 'py_m5serial'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='akariros',
    maintainer_email='akariros@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'M5publisher = src.m5stack_publisher:main',
            'client_color = src.py_m5client_color:main',
            'client_text = src.py_m5client_text:main',
            'service = src.py_m5server:main',
        ],
    },
)
