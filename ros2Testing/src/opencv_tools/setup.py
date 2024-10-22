from setuptools import find_packages, setup

package_name = 'opencv_tools'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='llagoeiro',
    maintainer_email='llagoeiro@outlook.com.br',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'publisherIMG = opencv_tools.PublisherIMGNode:main',
            'subscribeIMG = opencv_tools.SubscribeIMGNode:main',
            'subscribeYOLOIMG = opencv_tools.SubscribeIMGNodeYOLO:main'
        ],
    },
)
