# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import json

import pymel.core as pm

# Info
__author__ = 'Disco Hammer'
__copyright__ = 'Copyright 2017,  Dragon Unit Framestore LDN 2017'
__version__ = '0.1'
__email__ = 'gsorchin@framestore.com'
__status__ = 'Prototype'

# - Globals - #
tPREFIX = 'target_'
lPREFIX = 'loc_'


class CpSourceMesh(object):

    def __init__(self, mesh):
        self.name = mesh
        self.mesh = mesh.getChildren()[0]
        self.skin_cluster = self._get_skin_cluster()
        self.root_joint = self._get_root_joint()
        self.joint_hierarchy, self.joint_positions = self._get_joint_hierarchy(self.root_joint)
        self.loc_helpers = None
        self.vertex_weights = None

    # ---Private methods--- #

    def _get_skin_cluster(self):
        for node in self.mesh.connections():
            if node.nodeType() == 'skinCluster':
                return node

    def _get_root_joint(self):
        return self.skin_cluster.getInfluence()[0]

    def _get_joint_hierarchy(self, root_joint):

        hierarchy = dict()
        positions = dict()

        hierarchy[root_joint] = root_joint.getParent()
        positions[root_joint] = root_joint.getTranslation('world')

        for node in root_joint.listRelatives(allDescendents=True):
            if node.nodeType() == 'joint':
                hierarchy[node] = node.getParent()
                positions[node] = node.getTranslation('world')

        return hierarchy, positions

    # ---Public methods--- #

    def get_hierarchy(self):
        return self.joint_hierarchy

    def build_weights_association(self):
        """
        Associates weights and influences in the skin cluster per vertex.
        Handy for saving out skin weights or transferring them to a different mesh with the same topology.

        :return weights_association:
        :type weights_association: dict
        """
        self.vertex_weights = dict()
        threshold = 0.001

        for vtx in self.mesh.vtx:

            influence_name = pm.skinPercent(self.skin_cluster, vtx, transform=None, q=True, ib=threshold)
            influence_value = pm.skinPercent(self.skin_cluster, vtx, q=True, v=True, ib=threshold)

            # Encode unicode to str, so that we can export these values in the future
            vtx = str(vtx.name())
            influence_name = to_str(influence_name)

            self.vertex_weights[vtx] = zip(influence_name, influence_value)

    def export_vertex_weights(self):
        """
        Export the weight association to a json file for future use.
        :param source: The source skinned mesh
        :type source: CpSourceMesh
        :param filename: The desired name for the resulting json file
        :type filename: str
        :return res: str
        """
        if self.vertex_weights is not None:
           filename = pm.fileDialog2(fm=0)[0]
           res = write_json_file(self.vertex_weights, filename)
           return res
        else:
           return 'No pre-processed weights to export'


class CpTargetMesh(object):

    def __init__(self, mesh):
        self.name = mesh
        self.mesh = mesh.getChildren()[0]

        self.skin_cluster = self._get_skin_cluster()
        self.root_joint = None
        self.joints_connected = False
        self.joint_hierarchy = None
        self.joint_positions = None
        self.locs_and_joints = None
        # self.free_joints = None
        self.vertex_weights = None

    # --- Private methods --- #

    @staticmethod
    def _connect_joint(child, parent):

        pm.connectJoint(child, parent, pm=True)

    def _disconnect_joint(self, jnt):

        pm.disconnectJoint(jnt)

    def _get_joint_name(self, jnt):

        try:
            jnt_name = jnt.name()
        except AttributeError:
            jnt_name = None

        return jnt_name

    def _group_contents(self, grp_name, contents):

        pm.select(None)

        for element in contents:
            pm.select(element, add=True)

        grp = pm.group(name=grp_name)

    def _get_skin_cluster(self):
        for node in self.mesh.connections():
            if node.nodeType() == 'skinCluster':
                return node
            else:
                return None

    def _create_skin_cluster(self):
        self.skin_cluster = pm.skinCluster(self.locs_and_joints.values(), self.mesh)

    # --- Public methods --- #

    def build_help_locators(self, source_joint_dict):

        self.locs_and_joints = dict()

        for name, pos in source_joint_dict.iteritems():
            loc_name = lPREFIX + name
            loc = pm.spaceLocator(n=loc_name)
            loc.setTranslation((pos))

            jnt_name = tPREFIX + name
            pm.select(None)
            jnt = pm.joint(n=jnt_name)
            jnt.setRadius(0.2)
            jnt.setTranslation(loc.getTranslation('world'))

            self.locs_and_joints[loc] = jnt

        self._group_contents('grp_helpers', self.locs_and_joints.keys())

    def update_joints(self):

        if self.joints_connected:
            self.disconnect_joints()

        for loc, jnt in self.locs_and_joints.iteritems():
            jnt.setTranslation(loc.getTranslation('world'))

    def connect_joints(self, mapping):

        for child in mapping.keys():
            parent = mapping[child]
            if parent == None:
                pass
            else:
                src_child_name = self._get_joint_name(child)
                src_parent_name = self._get_joint_name(parent)

                trgt_child_name = tPREFIX + src_child_name
                trgt_parent_name = tPREFIX + src_parent_name

                self._connect_joint(trgt_child_name, trgt_parent_name)

        self.joints_connected = True

        '''        
        for jnt in self.locs_and_joints.values():

            jnt_name = self._get_joint_name(jnt)

            for child, parent in mapping.iteritems():

                child_name = self._get_joint_name(child)
                parent_name = self._get_joint_name(parent)

                if parent_name == None:
                    continue

                else:
                    if child_name in jnt_name:
                        print('Found!')
                        parent_name = 'jnt_' + parent_name
                        self._connect_joints(jnt_name, parent_name)
                    else:
                        print('Not Found!')
        '''

    def disconnect_joints(self):

        for joint in self.locs_and_joints.values():
            self._disconnect_joint(joint)

        self.joints_connected = False

    def import_vertex_weights(self):
        """
        Import skin weights previously saved out as json
        :param target: The target mesh
        :type target: CpTargetMesh
        :return: bool True if import succeeded
        """


        if self.skin_cluster == None:
            self._create_skin_cluster()

        file = pm.fileDialog2(fm=1)[0]

        vertex_data = readJsonFile(file)

        for key in sorted(vertex_data.keys()):
            target_key = key.replace('src_', 'target_')


        for keys, values in sorted(vertex_data.iteritems()):
            new_values = list()
            for pair in values:
                name, influence = pair
                name = tPREFIX + name
                new_values.append((name, influence))

        '''
        for vtx in self.mesh.vtx:

            influence_name = pm.skinPercent(self.skin_cluster, vtx, transform=None, q=True, ib=threshold)
            influence_value = pm.skinPercent(self.skin_cluster, vtx, q=True, v=True, ib=threshold)

            # Encode unicode to str, so that we can export these values in the future
            vtx = str(vtx.name())
            influence_name = to_str(influence_name)

            self.vertex_weights[vtx] = zip(influence_name, influence_value)
        '''
        self.vertex_weights = vertex_data

        if len(self.vertex_weights) > 0:

            for key in self.vertex_weights.keys():
                try:
                    pm.skinPercent(self.skin_cluster, key, tv=self.vertex_weights[key], zri=1)
                except Exception as e:
                    pm.displayError(e)

            '''
            for keys, values in self.vertex_weights.iteritems():
                new_values = list()
                for pair in values:
                    name, influence = pair
                    name = tPREFIX + name
                    new_values.append((name, influence))

                for key in keys:
                    new_key_name = key.replace('src_', 'target_')
                    try:
                        pm.skinPercent(self.skin_cluster, new_key_name, tv=new_values, zri=1)
                    except Exception as e:
                        pm.displayError(e)

            

            for key in self.vertex_weights.keys():
                formatted_names = list()
                names, values = self.vertex_weights[key]

                for name in names:
                    name = tPREFIX + name
                    formatted_names.append(name)
                try:
                    pm.skinPercent(self.skin_cluster, key, tv=(formatted_names, values), zri=1)
            '''

        else:
            pm.displayError('JSON file was empty')


# -- Decorators -- #


def cp_out_stamp(console):
    def wrapper(*args):
        return "[Cranium-Post]: <<< {0}".format(args[0])

    return wrapper


# --- Public functions --- #

def copy_skin(source, target, same_topology=True):
    """
    Copy the source skin behaviour to the target mesh.
    If the topology is the same, a "copy influences per vertex" approach is taken, otherwise,
    maya's CopySkinWeights is used.

    :param source: Source skinned mesh
    :type source: CpSourceMesh
    :param target: Target non skinned mesh (target rig must be present)
    :type target: CpTargetMesh
    :param same_topology: Flags whether the the topology in both meshes is the same or not
    :type same_topology: bool
    """
    #TODO

    pass

# These functions are implemented as public methods for the relevant classes
'''
def export_vertex_weights(source):
    """
    Export the weight association to a json file for future use.
    :param source: The source skinned mesh
    :type source: CpSourceMesh
    :param filename: The desired name for the resulting json file
    :type filename: str
    :return: bool True if file writing succeeded
    """
    if source.vertex_weights is not None:
        filename = pm.fileDialog2(fm=0)[0]
        write_json_file(source.vertex_weights, filename)
    else:
        return

def import_vertex_weights(target):
    """
    Import skin weights previously saved out as json
    :param target: The target mesh
    :type target: CpTargetMesh
    :return: bool True if import succeeded
    """
'''


def set_as_source():

    try:
        source = pm.ls(selection=True)[0]
    except IndexError:
        raise AttributeError
    else:
        source = CpSourceMesh(source)  # May rise AttributeError
        return source


def set_as_target():

    try:
        target = pm.ls(selection=True)[0]
    except IndexError:
        raise AttributeError
    else:
        target = CpTargetMesh(target)  # May rise AttributeError
        return target


def get_skin_cluster(mesh):

    #selection = pm.ls(selection=True)[0]
    shape = mesh.getChildren()[0]
    skin_cluster = None

    for node in shape.connections():
        if node.nodeType() == 'skinCluster':
            skin_cluster = node
            break

    return skin_cluster


def get_joint_hierarchy(root_joint):
    # Get Joint Hierarchy, returns two dicts joint hierarchy and joint positions

    hierarchy = dict()
    positions = dict()

    hierarchy[root_joint] = root_joint.getParent()
    positions[root_joint] = root_joint.getTranslation('world')

    for node in root_joint.listRelatives(allDescendents=True):
        if node.nodeType() == 'joint':
            hierarchy[node] = node.getParent()
            positions[node] = node.getTranslation('world')

    return hierarchy, positions


def file_dialog(**kwargs):
    """ Presents the user with a maya file dialog window
        Returns the file name as a string """

    file = pm.fileDialog2(**kwargs)[0]  # Index the first file from list

    if not os.path.isfile(file):
        return '[Cp-Ops]: Please select a valid file.'

    else:
        return '[Cp-Ops]: ' + file


def import_file(file_name, **kwargs):
    """ Import a file into the scene """

    file_name = to_str(file_name)

    return pm.importFile(file_name, **kwargs)


def save_file(file_name, **kwargs):
    """ Save current file """

    file_name = to_str(file_name)

    return pm.saveFile(file_name, **kwargs)


@cp_out_stamp
def to_console(msg):
    return msg




# -- Utility functions Start --- #
# JSON
def write_json_file(dataToWrite, fileName):
    if '.json' not in fileName:
        fileName += '.json'

    with open(fileName, "w") as json_file:
        try:
            json.dump(dataToWrite, json_file, indent=2)
        except Exception as e:
            return e
        else:
            return 'Data was successfully written to {0}'.format(fileName)


# JSON
def readJsonFile(fileName):
    # type: (object) -> object
    with open(fileName, 'r') as json_file:
        try:
            data = json.load(json_file)
        except Exception as e:
            print("Could not read {0} {1}".format(fileName, e))
        else:
            return data
# Python 2
def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str
    return value  # Instance of unicode

# Python 2
def to_str(unicode_or_str):
    if isinstance(unicode_or_str, unicode):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value  # Instance of str

# -- Utility functions End --- #

test_string = 'Disco Fox'
val1 = to_unicode(test_string)
val2 = to_str(test_string)