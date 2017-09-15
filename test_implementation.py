from __future__ import print_function

from cp_ops import cp_file_ops;

reload(cp_file_ops)

import pymel.core as pm

source = pm.ls(selection=True)[0]
source = cp_file_ops.CpSourceMesh(source)

target = pm.ls(selection=True)[0]
target = cp_file_ops.CpTargetMesh(target)

print(source.joint_hierarchy)

target.build_help_locators(source.joint_positions)

target.update_joints()

target.connect_joints(source.joint_hierarchy)

target._create_skin_cluster()


