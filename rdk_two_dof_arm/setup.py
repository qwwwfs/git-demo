from glob import glob
from setuptools import setup

setup(
    name="rdk_arm", version="0.1.0", packages=["rdk_arm"],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/rdk_arm"]),
        ("share/rdk_arm", ["package.xml"]),
        ("share/rdk_arm/launch", glob("launch/*.launch.py")),
        ("share/rdk_arm/config", glob("config/*.yaml")),
    ],
    install_requires=["setuptools"], zip_safe=True,
    maintainer="Project Maintainer", maintainer_email="maintainer@example.com",
    description="Two-joint ROS2 simulation scaffold for RDK deployment",
    license="UNLICENSED",
    entry_points={"console_scripts": [
        "arm_controller = rdk_arm.arm_node:main", "demo = rdk_arm.demo:main"
    ]},
)
