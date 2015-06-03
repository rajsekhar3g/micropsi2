from micropsi_core.world.worldadapter import WorldAdapter
from micropsi_core import tools
from configuration import config as cfg
import random
import logging
import time
from functools import partial
from math import sqrt, radians, cos, sin, tan


class MinecraftVision(WorldAdapter):

    supported_datasources = []

    supported_datatargets = [
        'take_exit_one',
        'take_exit_two',
        'take_exit_three',
        'pitch',
        'yaw',
        'fov_x',
        'fov_y',
        'res_x',
        'res_y',
        'len_x',
        'len_y'
    ]

    loco_node_template = {
        'uid': "",
        'name': "",
        'x': 0,
        'y': 0,
        'z': 0,
        'exit_one_uid': None,
        'exit_two_uid': None,
        'exit_three_uid': None,
    }

    loco_nodes = {}

    home_uid = tools.generate_uid()
    underground_garden_uid = tools.generate_uid()
    village_uid = tools.generate_uid()
    cathedral_uid = tools.generate_uid()
    summit_uid = tools.generate_uid()
    cloud_uid = tools.generate_uid()
    bungalow_uid = tools.generate_uid()
    farm_uid = tools.generate_uid()
    forest_uid = tools.generate_uid()
    desert_outpost_uid = tools.generate_uid()
    swamp_uid = tools.generate_uid()

    loco_nodes_indexes = [None, 'home', 'underground garden', 'village', 'cathedral', 'summit',
                          'cloud', 'bungalow', 'farm', 'forest', 'desert outpost', 'swamp']

    loco_nodes[home_uid] = loco_node_template.copy()
    loco_nodes[home_uid]['name'] = "home"
    loco_nodes[home_uid]['uid'] = home_uid
    loco_nodes[home_uid]['x'] = -105
    loco_nodes[home_uid]['y'] = 63
    loco_nodes[home_uid]['z'] = 59
    loco_nodes[home_uid]['exit_one_uid'] = cloud_uid
    loco_nodes[home_uid]['exit_two_uid'] = cathedral_uid
    loco_nodes[home_uid]['exit_three_uid'] = village_uid

    loco_nodes[underground_garden_uid] = loco_node_template.copy()
    loco_nodes[underground_garden_uid]['name'] = "underground garden"
    loco_nodes[underground_garden_uid]['uid'] = underground_garden_uid
    loco_nodes[underground_garden_uid]['x'] = -264
    loco_nodes[underground_garden_uid]['y'] = 62
    loco_nodes[underground_garden_uid]['z'] = 65
    loco_nodes[underground_garden_uid]['exit_one_uid'] = home_uid
    loco_nodes[underground_garden_uid]['exit_two_uid'] = village_uid

    loco_nodes[village_uid] = loco_node_template.copy()
    loco_nodes[village_uid]['name'] = "village"
    loco_nodes[village_uid]['uid'] = village_uid
    loco_nodes[village_uid]['x'] = -293
    loco_nodes[village_uid]['y'] = 64
    loco_nodes[village_uid]['z'] = -220
    loco_nodes[village_uid]['exit_one_uid'] = underground_garden_uid
    loco_nodes[village_uid]['exit_two_uid'] = home_uid

    loco_nodes[cathedral_uid] = loco_node_template.copy()
    loco_nodes[cathedral_uid]['name'] = "cathedral"
    loco_nodes[cathedral_uid]['uid'] = cathedral_uid
    loco_nodes[cathedral_uid]['x'] = -100
    loco_nodes[cathedral_uid]['y'] = 63
    loco_nodes[cathedral_uid]['z'] = 282
    loco_nodes[cathedral_uid]['exit_one_uid'] = home_uid
    loco_nodes[cathedral_uid]['exit_two_uid'] = cloud_uid
    loco_nodes[cathedral_uid]['exit_three_uid'] = bungalow_uid

    loco_nodes[summit_uid] = loco_node_template.copy()
    loco_nodes[summit_uid]['name'] = "summit"
    loco_nodes[summit_uid]['uid'] = summit_uid
    loco_nodes[summit_uid]['x'] = -233
    loco_nodes[summit_uid]['y'] = 102
    loco_nodes[summit_uid]['z'] = 307
    loco_nodes[summit_uid]['exit_one_uid'] = swamp_uid

    loco_nodes[cloud_uid] = loco_node_template.copy()
    loco_nodes[cloud_uid]['name'] = "cloud"
    loco_nodes[cloud_uid]['uid'] = cloud_uid
    loco_nodes[cloud_uid]['x'] = -98
    loco_nodes[cloud_uid]['y'] = 63
    loco_nodes[cloud_uid]['z'] = 198
    loco_nodes[cloud_uid]['exit_one_uid'] = home_uid
    loco_nodes[cloud_uid]['exit_two_uid'] = cathedral_uid

    loco_nodes[bungalow_uid] = loco_node_template.copy()
    loco_nodes[bungalow_uid]['name'] = "bungalow"
    loco_nodes[bungalow_uid]['uid'] = bungalow_uid
    loco_nodes[bungalow_uid]['x'] = 28
    loco_nodes[bungalow_uid]['y'] = 63
    loco_nodes[bungalow_uid]['z'] = 292
    loco_nodes[bungalow_uid]['exit_one_uid'] = cathedral_uid
    loco_nodes[bungalow_uid]['exit_two_uid'] = farm_uid

    loco_nodes[farm_uid] = loco_node_template.copy()
    loco_nodes[farm_uid]['name'] = "farm"
    loco_nodes[farm_uid]['uid'] = farm_uid
    loco_nodes[farm_uid]['x'] = -50
    loco_nodes[farm_uid]['y'] = 64
    loco_nodes[farm_uid]['z'] = 410
    loco_nodes[farm_uid]['exit_one_uid'] = bungalow_uid
    loco_nodes[farm_uid]['exit_two_uid'] = cathedral_uid
    loco_nodes[farm_uid]['exit_three_uid'] = forest_uid

    loco_nodes[forest_uid] = loco_node_template.copy()
    loco_nodes[forest_uid]['name'] = "forest"
    loco_nodes[forest_uid]['uid'] = forest_uid
    loco_nodes[forest_uid]['x'] = -273
    loco_nodes[forest_uid]['y'] = 65
    loco_nodes[forest_uid]['z'] = 782
    loco_nodes[forest_uid]['exit_one_uid'] = farm_uid
    loco_nodes[forest_uid]['exit_two_uid'] = desert_outpost_uid
    loco_nodes[forest_uid]['exit_three_uid'] = swamp_uid

    loco_nodes[desert_outpost_uid] = loco_node_template.copy()
    loco_nodes[desert_outpost_uid]['name'] = "desert outpost"
    loco_nodes[desert_outpost_uid]['uid'] = desert_outpost_uid
    loco_nodes[desert_outpost_uid]['x'] = -243
    loco_nodes[desert_outpost_uid]['y'] = 64
    loco_nodes[desert_outpost_uid]['z'] = 958
    loco_nodes[desert_outpost_uid]['exit_one_uid'] = forest_uid

    loco_nodes[swamp_uid] = loco_node_template.copy()
    loco_nodes[swamp_uid]['name'] = "swamp"
    loco_nodes[swamp_uid]['uid'] = swamp_uid
    loco_nodes[swamp_uid]['x'] = -529
    loco_nodes[swamp_uid]['y'] = 63
    loco_nodes[swamp_uid]['z'] = 504
    loco_nodes[swamp_uid]['exit_one_uid'] = forest_uid
    loco_nodes[swamp_uid]['exit_two_uid'] = summit_uid

    tp_tolerance = 5
    action_timeout = 10
    actions = ['take_exit_one', 'take_exit_two', 'take_exit_three']

    logger = None

    # specs for vision /fovea
    # image width and height define the part of the world that can be viewed
    # ie. they provide the proportions of the projection /image plane in the world
    im_width = 128
    im_height = 64
    # camera values define width and height of the normalized device /camera /viewport
    cam_width = 1.
    cam_height = 1.
    # focal length defines the distance between the image plane and the projective point /fovea
    # ( focal length > 0 means zooming in, < 0 means zooming out;
    #   small values distort the image, in particular if objects are close )
    focal_length = 0.5
    # the maximal distance for raytracing -- the value was determined by manually trying several values
    max_dist = 64

    # # the patch size required to cover the complete visual field of 128 x 64 blocks
    # zoom_levels = {
    #     1: (0.125, 0.25),  # 16 x 16 - fairly coarse
    #     2: (0.25, 0.5),    # 32 x 32 -
    #     3: (0.5, 1.0)      # 64 x 64 - how fine ?
    # }

    # the max number of fovea sensors to instantiate; should be smaller or equal to resolution x image dimension
    num_pix_x = 16
    num_pix_y = 16

    # cf. autoencoders require similar activation ( up to noise ) for three consecutive steps
    num_steps_to_keep_vision_stable = 3

    def __init__(self, world, uid=None, **data):
        super(MinecraftVision, self).__init__(world, uid, **data)

        self.datatarget_feedback = {
            'take_exit_one': 0,
            'take_exit_two': 0,
            'take_exit_three': 0,
            'fov_x': 0,
            'fov_y': 0,
            'res_x': 0,
            'res_y': 0,
            'len_x': 0,
            'len_y': 0
        }

        # prevent instabilities in datatargets: treat a continuous ( /unintermittent ) signal as a single trigger
        self.datatarget_history = {
            'take_exit_one': 0,
            'take_exit_two': 0,
            'take_exit_three': 0,
            'fov_x': 0,
            'fov_y': 0,
            'res_x': 0,
            'res_y': 0,
            'len_x': 0,
            'len_y': 0
        }

        # a collection of conditions to check on every update(..), eg., for action feedback
        self.waiting_list = []

        self.target_loco_node_uid = None
        self.current_loco_node = None

        self.spockplugin = self.world.spockplugin
        self.waiting_for_spock = True
        self.logger = logging.getLogger("world")

        # add datasources for fovea sensors aka fov__*_*
        for i in range(self.num_pix_x):
            for j in range(self.num_pix_y):
                name = "fov__%02d_%02d" % (i, j)
                self.datasources[name] = 0.

        self.simulated_vision = False
        if 'simulate_vision' in cfg['minecraft']:
            self.simulated_vision = True
            self.simulated_vision_datafile = cfg['minecraft']['simulate_vision']
            self.logger.info("Setting up minecraft_graph_locomotor to simulate vision from data file %s", self.simulated_vision_datafile)

            import os
            import csv
            self.simulated_vision_data = None
            self.simulated_vision_datareader = csv.reader(open(self.simulated_vision_datafile))
            if os.path.getsize(self.simulated_vision_datafile) < (500 * 1024 * 1024):
                self.simulated_vision_data = [[float(datapoint) for datapoint in sample] for sample in self.simulated_vision_datareader]
                self.simulated_data_entry_index = 0
                self.simulated_data_entry_max = len(self.simulated_vision_data) - 1

        if 'record_vision' in cfg['minecraft']:
            self.record_file = open(cfg['minecraft']['record_vision'], 'a')

    def update_data_sources_and_targets(self):
        """called on every world simulation step to advance the life of the agent"""

        # first thing when spock initialization is done, determine current loco node
        if self.waiting_for_spock:
            # by substitution: spock init is considered done, when its client has a position unlike
            # {'on_ground': False, 'pitch': 0, 'x': 0, 'y': 0, 'yaw': 0, 'stance': 0, 'z': 0}:
            if not self.simulated_vision:
                if self.spockplugin.clientinfo.position['y'] != 0. \
                        and self.spockplugin.clientinfo.position['x'] != 0:
                    self.waiting_for_spock = False
                    x = int(self.spockplugin.clientinfo.position['x'])
                    y = int(self.spockplugin.clientinfo.position['y'])
                    z = int(self.spockplugin.clientinfo.position['z'])
                    for k, v in self.loco_nodes.items():
                        if abs(x - v['x']) <= self.tp_tolerance \
                           and abs(y - v['y']) <= self.tp_tolerance \
                           and abs(z - v['z']) <= self.tp_tolerance:
                            self.current_loco_node = self.loco_nodes[k]

                    if self.current_loco_node is None:
                        # bot is outside our graph, teleport to a random graph location to get started.
                        target = random.choice(list(self.loco_nodes.keys()))
                        self.locomote(target)
                    # self.locomote(self.village_uid)
            else:
                self.waiting_for_spock = False
        else:

            # reset self.datatarget_feedback
            for k in self.datatarget_feedback.keys():
                # reset actions only if not requested anymore
                if k in self.actions:
                    if self.datatargets[k] == 0:
                        self.datatarget_feedback[k] = 0.
                else:
                    self.datatarget_feedback[k] = 0.

            if not self.simulated_vision:

                if not self.spockplugin.is_connected():
                    return

                # change pitch and yaw every x world steps to increase sensory variation
                # < ensures some stability to enable learning in the autoencoder
                if self.world.current_step % self.num_steps_to_keep_vision_stable == 0:
                    # for patches pitch = 10 and yaw = random.randint(-10,10) were used
                    # for visual field pitch = randint(0, 30) and yaw = randint(1, 360) were used
                    self.spockplugin.clientinfo.position['pitch'] = 10
                    self.spockplugin.clientinfo.position['yaw'] = random.randint(-10, 10)
                    self.datatargets['pitch'] = self.spockplugin.clientinfo.position['pitch']
                    self.datatargets['yaw'] = self.spockplugin.clientinfo.position['yaw']
                    # Note: datatargets carry spikes not continuous signals, ie. pitch & yaw will be 0 in the next step
                    self.datatarget_feedback['pitch'] = 1.0
                    self.datatarget_feedback['yaw'] = 1.0

                # sample all the time
                self.datasources['fov_x'] = self.datatargets['fov_x'] - 1. if self.datatargets['fov_x'] > 0. else 0.
                self.datasources['fov_y'] = self.datatargets['fov_y'] - 1. if self.datatargets['fov_y'] > 0. else 0.
                loco_label = self.current_loco_node['name']  # because python uses call-by-object
                self.get_visual_input(self.datatargets['fov_x'], self.datatargets['fov_y'],
                                      self.datatargets['res_x'], self.datatargets['res_y'],
                                      int(self.datatargets['len_x']), int(self.datatargets['len_y']), loco_label)

                # Note: saccading can't fail because fov_x, fov_y are internal actors, hence we return immediate feedback
                if self.datatargets['fov_x'] > 0.0:
                    self.datatarget_feedback['fov_x'] = 1.0
                if self.datatargets['fov_y'] > 0.0:
                    self.datatarget_feedback['fov_y'] = 1.0

                self.check_for_action_feedback()

                # read locomotor values, trigger teleportation in the world, and provide action feedback
                # don't trigger another teleportation if the datatargets was on continuously, cf. pipe logic
                if self.datatargets['take_exit_one'] >= 1 and not self.datatarget_history['take_exit_one'] >= 1:
                    # if the current node on the transition graph has the selected exit
                    if self.current_loco_node['exit_one_uid'] is not None:
                        self.register_action(
                            'take_exit_one',
                            partial(self.locomote, self.current_loco_node['exit_one_uid']),
                            partial(self.check_movement_feedback, self.current_loco_node['exit_one_uid'])
                        )
                    else:
                        self.datatarget_feedback['take_exit_one'] = -1.

                if self.datatargets['take_exit_two'] >= 1 and not self.datatarget_history['take_exit_two'] >= 1:
                    if self.current_loco_node['exit_two_uid'] is not None:
                        self.register_action(
                            'take_exit_two',
                            partial(self.locomote, self.current_loco_node['exit_two_uid']),
                            partial(self.check_movement_feedback, self.current_loco_node['exit_two_uid'])
                        )
                    else:
                        self.datatarget_feedback['take_exit_two'] = -1.

                if self.datatargets['take_exit_three'] >= 1 and not self.datatarget_history['take_exit_three'] >= 1:
                    if self.current_loco_node['exit_three_uid'] is not None:
                        self.register_action(
                            'take_exit_three',
                            partial(self.locomote, self.current_loco_node['exit_three_uid']),
                            partial(self.check_movement_feedback, self.current_loco_node['exit_three_uid'])
                        )
                    else:
                        self.datatarget_feedback['take_exit_three'] = -1.

                # update datatarget history
                for k in self.datatarget_history.keys():
                    self.datatarget_history[k] = self.datatargets[k]

            else:
                self.simulate_visual_input(self.num_pix_x, self.num_pix_y)

    def locomote(self, target_loco_node_uid):
        new_loco_node = self.loco_nodes[target_loco_node_uid]

        self.logger.debug('locomoting to  %s' % new_loco_node['name'])

        self.spockplugin.chat("/tppos {0} {1} {2}".format(
            new_loco_node['x'],
            new_loco_node['y'],
            new_loco_node['z']))

        self.target_loco_node_uid = target_loco_node_uid

        self.current_loco_node = new_loco_node

    def check_for_action_feedback(self):
        """ """
        # check if any pending datatarget_feedback can be confirmed with data from the world
        if self.waiting_list:
            new_waiting_list = []
            for index, item in enumerate(self.waiting_list):
                if item['validation']():
                    if self.datatargets[item['datatarget']] != 0:
                        self.datatarget_feedback[item['datatarget']] = 1.
                else:
                    new_waiting_list.append(item)

            self.waiting_list = new_waiting_list

    def register_action(self, datatarget, action_function, validation_function):
        """ Registers an action to be performed by the agent. Will wait, and eventually re-trigger the action
            until the validation function returns true, signalling success of the action"""
        self.waiting_list.append({
            'datatarget': datatarget,
            'action': action_function,
            'validation': validation_function,
            'time': time.clock()
        })
        action_function()

    def check_movement_feedback(self, target_loco_node):
        if abs(self.loco_nodes[target_loco_node]['x'] - int(self.spockplugin.clientinfo.position['x'])) <= self.tp_tolerance \
           and abs(self.loco_nodes[target_loco_node]['y'] - int(self.spockplugin.clientinfo.position['y'])) <= self.tp_tolerance \
           and abs(self.loco_nodes[target_loco_node]['z'] - int(self.spockplugin.clientinfo.position['z'])) <= self.tp_tolerance:
            return True
        return False

    def get_visual_input(self, fov_x, fov_y, res_x, res_y, len_x, len_y, label):
        """
        Spans an image plane ( of size ... ), selects a patch on that image plane
        starting from (fov_x, fov_y) and of size (len_x, len_y) and raytraces
        in the Minecraft block world to fill that patch with block type values
        of a 2D perspective projection.

        Order of traversal: left to right, top to bottom ( before rotation );
        that is fov_00_00 gets the top left pixel.
        """
        if res_x == 0.0 or res_y == 0.0 or len_x == 0.0 or len_y == 0.0:
            return

        # get agent position
        pos_x = self.spockplugin.clientinfo.position['x']
        pos_y = self.spockplugin.clientinfo.position['y'] + 0.620  # add some stance to y pos ( which is ground + 1 )
        pos_z = self.spockplugin.clientinfo.position['z']

        # get yaw and pitch ( in degrees )
        yaw = self.spockplugin.clientinfo.position['yaw']
        pitch = self.spockplugin.clientinfo.position['pitch']

        # compute ticks per dimension
        tick_w = self.cam_width / self.im_width / res_x
        tick_h = self.cam_height / self.im_height / res_y

        # span image plane
        # the horizontal plane is split half-half, the vertical plane is shifted upwards
        h_line = [i for i in self.frange(pos_x - 0.5 * self.cam_width, pos_x + 0.5 * self.cam_width, tick_w)]
        v_line = [i for i in self.frange(pos_y - 0.05 * self.cam_height, pos_y + 0.95 * self.cam_height, tick_h)]

        # scale up fov_x, fov_y - which is originally in the domain [0,1]
        fov_x = int(round(fov_x * (self.im_width * res_x - len_x)))
        fov_y = int(round(fov_y * (self.im_height * res_y - len_y)))

        x0, y0, z0 = pos_x, pos_y, pos_z  # agent's position aka projective point
        zi = z0 + self.focal_length

        v_line.reverse()  # inline

        # do raytracing to compute the resp. block type values of a 2D perspective projection
        sensor_values = []
        for i in range(len_x):
            for j in range(len_y):
                try:
                    block_type, distance = self.project(h_line[fov_x + j], v_line[fov_y + i], zi, x0, y0, z0, yaw, pitch)
                except IndexError:
                    block_type, distance = -1, -1
                    self.logger.warning("IndexError at (%d,%d)" % (fov_x + j, fov_y + i))
                sensor_values.append(block_type)

        # homogeneous_patch = False
        # if sensor_values[1:] == sensor_values[:-1]:  # if all sensor values are the same, ignore the sample ie. write zeros
        #     homogeneous_patch = True
        #     norm_sensor_values = [0.0] * len_x * len_y

        # else:  # else normalize the sensor values
        norm_sensor_values = self.normalize_sensor_values(sensor_values)

        # write new sensor values to datasources
        self.write_visual_input_to_datasources(norm_sensor_values, len_x, len_y)

        if 'record_vision' in cfg['minecraft']:
            # do *not* record homogeneous and replayed patches
            if not self.simulated_vision:  # if not homogeneous_patch and not self.simulated_vision:
                if label == self.current_loco_node['name']:
                    data = "{0}".format(",".join(str(b) for b in sensor_values))
                    self.record_file.write("%s,%s,%d,%d,%d,%d,%.3f,%.3f,%d,%d\n" %
                                           (data, label, pitch, yaw, fov_x, fov_y, res_x, res_y, len_x, len_y))
                else:
                    self.logger.warn('potentially corrupt data were ignored')

    def simulate_visual_input(self, len_x, len_y):
        """
        Every <self.num_steps_to_keep_vision_stable> steps read the next line
        from the vision file and fill its values into fov__*_* datasources.
        """
        if self.world.current_step % self.num_steps_to_keep_vision_stable == 0:
            line = None
            if self.simulated_vision_data is None:
                line = next(self.simulated_vision_datareader, None)
                if line is None:
                    self.logger.info("Simulating vision from data file, starting over...")
                    import csv
                    self.simulated_vision_datareader = csv.reader(open(self.simulated_vision_datafile))
                    line = next(self.simulated_vision_datareader)
                line = [float(entry) for entry in line]
            else:
                self.simulated_data_entry_index += 1
                if self.simulated_data_entry_index > self.simulated_data_entry_max:
                    self.logger.info("Simulating vision from memory, starting over, %s entries.", self.simulated_data_entry_max + 1)
                    self.simulated_data_entry_index = 0
                line = self.simulated_vision_data[self.simulated_data_entry_index]
            self.write_visual_input_to_datasources(line, len_x, len_y)

    def write_visual_input_to_datasources(self, sensor_values, len_x, len_y):
        """
        Write computed fovea sensor values to the respective datasources fov__*_*.
        """
        for x in range(len_x):
            for y in range(len_y):
                name = 'fov__%02d_%02d' % (x, y)
                self.datasources[name] = sensor_values[(len_y * x) + y]

    def normalize_sensor_values(self, patch):
        """
        Normalize sensor values to zero mean and 3 standard deviation.
        TODO: make doc correct and precise.
        """
        # convert block types into binary values: map air and emptiness to black (0), everything else to white (1)
        patch_ = [0.0 if v <= 0 else 1.0 for v in patch]

        # normalize block type values
        # subtract the sample mean from each of its pixels
        mean = float(sum(patch_)) / len(patch_)
        patch_avg = [x - mean for x in patch_]  # TODO: throws error in ipython - why not here !?

        # truncate to +/- 3 standard deviations and scale to -1 and +1

        var = [x ** 2.0 for x in patch_avg]
        std = (sum(var) / len(var)) ** 0.5  # ASSUMPTION: all values of x are equally likely
        pstd = 3.0 * std
        # if block types are all the same number, eg. -1, std will be 0, therefore
        if pstd == 0.0:
            patch_std = [0.0 for x in patch_avg]
        else:
            patch_std = [max(min(x, pstd), -pstd) / pstd for x in patch_avg]

        # scale from [-1,+1] to [0.1,0.9] and write values to sensors
        patch_resc = [(1.0 + x) * 0.4 + 0.1 for x in patch_std]
        return patch_resc

    def project(self, xi, yi, zi, x0, y0, z0, yaw, pitch):
        """
        Given a point on the projection plane and the agent's position, cast a
        ray to find the nearest block type that isn't air and its distance from
        the projective plane.
        """
        distance = 0    # just a counter
        block_type = -1  # consider mapping nothingness to air, ie. -1 to 0

        # compute difference vector between projective point and image point
        diff = (xi - x0, yi - y0, zi - z0)

        # normalize difference vector
        magnitude = sqrt(diff[0] ** 2 + diff[1] ** 2 + diff[2] ** 2)
        if magnitude == 0.:
            magnitude = 1.
        norm = (diff[0] / magnitude, diff[1] / magnitude, diff[2] / magnitude)

        # rotate norm vector
        norm = self.rotate_around_x_axis(norm, pitch)
        norm = self.rotate_around_y_axis(norm, yaw)

        # rotate diff vector
        diff = self.rotate_around_x_axis(diff, pitch)
        diff = self.rotate_around_y_axis(diff, yaw)

        # add diff to projection point aka agent's position
        xb, yb, zb = x0 + diff[0], y0 + diff[1], z0 + diff[2]

        while block_type <= 0:  # which is air and nothingness

            # check block type of next distance point along ray
            # aka add normalized difference vector to image point
            # TODO: consider a more efficient way to move on the ray, eg. a log scale
            xb += norm[0]
            yb += norm[1]
            zb += norm[2]

            block_type = self.spockplugin.get_block_type(xb, yb, zb)

            distance += 1
            if distance >= self.max_dist:
                break

        return block_type, distance

    def rotate_around_x_axis(self, pos, angle):
        """ Rotate a 3D point around the x-axis given a specific angle. """

        # convert angle in degrees to radians
        theta = radians(angle)

        # rotate vector
        xx, y, z = pos
        yy = y * cos(theta) - z * sin(theta)
        zz = y * sin(theta) + z * cos(theta)

        return (xx, yy, zz)

    def rotate_around_y_axis(self, pos, angle):
        """ Rotate a 3D point around the y-axis given a specific angle. """

        # convert angle in degrees to radians
        theta = radians(angle)

        # rotate vector
        x, yy, z = pos
        xx = x * cos(theta) + z * sin(theta)
        zz = - x * sin(theta) + z * cos(theta)

        return (xx, yy, zz)

    def rotate_around_z_axis(self, pos, angle):
        """ Rotate a 3D point around the z-axis given a specific angle. """

        # convert angle in degrees to radians
        theta = radians(angle)

        # rotate vector
        x, y, zz = pos
        xx = x * cos(theta) - y * sin(theta)
        yy = x * sin(theta) + y * cos(theta)

        return (xx, yy, zz)

    def frange(self, start, end, step):
        """
        Range for floats.
        """
        while start < end:
            yield start
            start += step
