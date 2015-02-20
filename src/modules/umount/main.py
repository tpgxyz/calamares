#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014, Aurélien Gâteau <agateau@kde.org>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess

import libcalamares


def list_mounts(root_mount_point):
    """

    :param root_mount_point:
    :return:
    """
    lst = []
    for line in open("/etc/mtab").readlines():
        device, mount_point, _ = line.split(" ", 2)
        if mount_point.startswith(root_mount_point):
            lst.append((device, mount_point))
    return lst


def run():
    """


    :return:
    """
    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")
    if not root_mount_point:
        return ("No mount point for root partition in globalstorage",
                "globalstorage does not contain a \"rootMountPoint\" key, "
                "doing nothing")
    if not os.path.exists(root_mount_point):
        return ("Bad mount point for root partition in globalstorage",
                "globalstorage[\"rootMountPoint\"] is \"{}\", which does not "
                "exist, doing nothing".format(root_mount_point))

    lst = list_mounts(root_mount_point)
    # Sort the list by mount point in decreasing order. This way we can be sure
    # we unmount deeper dirs first.
    lst.sort(key=lambda x: x[1], reverse=True)

    for device, mount_point in lst:
        subprocess.check_call(["umount", "-lv", mount_point])

    os.rmdir(root_mount_point)
    return None
