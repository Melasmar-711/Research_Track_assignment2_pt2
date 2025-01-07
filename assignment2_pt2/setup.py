from setuptools import setup

package_name = 'assignment2_pt2'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    py_modules=[
   'move_robot',
   'move_robot_updated',
    ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/launch_sim.launch.py']),
        ('share/' + package_name + '/launch', ['launch/launch_the_correct_sim.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='asmar',
    maintainer_email='Mahmoudelasmar2000@outlook.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'move_robot=move_robot:main',
        'move_robot_updated=move_robot_updated:main'
        ],
    },
)
