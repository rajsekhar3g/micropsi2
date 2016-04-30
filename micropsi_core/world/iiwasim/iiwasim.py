import math
import os
import logging
from micropsi_core.world.iiwasim import vrep
from micropsi_core.world.iiwasim import vrepConst
from micropsi_core.world.world import World
from micropsi_core.world.worldadapter import ArrayWorldAdapter


class iiwasim(World):
    """ A simulated KUKA iiwa, using the vrep robot simulator

        In V-REP, the following setup has to be performed:
        - An LBR_iiwa_7_R800 has to have been added to the scene
        - simExtRemoteApiStart(19999) has to have been run
        - the simulation must have been started

    """

    supported_worldadapters = ['iiwa']

    def __init__(self, filename, world_type="iiwasim", name="", owner="", engine=None, uid=None, version=1, config={}):
        World.__init__(self, filename, world_type=world_type, name=name, owner=owner, uid=uid, version=version)

        vrep.simxFinish(-1) # just in case, close all opened connections
        self.clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5) # Connect to V-REP
        if self.clientID == -1:
            raise Exception("Could not connect to v-rep.")

        self.logger.info("Connected to local V-REP at port 19999")

        res, pingtime = vrep.simxGetPingTime(self.clientID)
        self.handle_res(res)

        self.logger.info('Ping time to v-rep: %dms' % pingtime)

        res, self.iiwa_handle = vrep.simxGetObjectHandle(self.clientID, "LBR_iiwa_7_R800", vrep.simx_opmode_blocking)
        self.handle_res(res)
        if self.iiwa_handle == 0:
            raise Exception("There seems to be no robot with the name LBR_iiwa_7_R800 in the v-rep simulation.")

        res, self.joints = vrep.simxGetObjects(self.clientID, vrep.sim_object_joint_type, vrep.simx_opmode_blocking)
        self.handle_res(res)
        if len(self.joints) != 7:
            raise Exception("Could not get handles for all 7 joints of the LBR_iiwa_7_R800.")

    def handle_res(self, res):
        if res != vrep.simx_return_ok:
            self.logger.warn("v-rep call returned error code %d" % res)


class iiwa(ArrayWorldAdapter):

    def __init__(self, world, uid=None, **data):
        super().__init__(world, uid, **data)

        self.available_datatargets = []
        self.available_datasources = []

        for i in range(len(self.world.joints)):
            self.available_datatargets.append("joint_%d" % i)

    def get_available_datasources(self):
        return self.available_datasources

    def get_available_datatargets(self):
        return self.available_datatargets

    def update_data_sources_and_targets(self):
        vrep.simxPauseCommunication(self.world.clientID, True)
        for i, joint_handle in enumerate(self.world.joints):
            tval = self.datatarget_values[i] * math.pi
            vrep.simxSetJointTargetPosition(self.world.clientID, joint_handle, tval, vrep.simx_opmode_oneshot)
        vrep.simxPauseCommunication(self.world.clientID, False)

        res, joint_ids, something, data, se = vrep.simxGetObjectGroupData(self.world.clientID, vrep.sim_object_joint_type, 15, vrep.simx_opmode_blocking)
        self.datatarget_feedback_values = [0] * len(self.available_datatargets)
        for i, joint_handle in enumerate(self.world.joints):
            tval = self.datatarget_values[i]
            rval = data[i*2] / math.pi
            if abs(rval) - abs(tval) < .0001:
                self.datatarget_feedback_values[i] = 1
