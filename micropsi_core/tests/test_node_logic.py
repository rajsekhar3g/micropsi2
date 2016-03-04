#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Tests for node activation propagation and gate arithmetic
"""

from micropsi_core import runtime as micropsi


def prepare(test_nodenet):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    source = netapi.create_node("Register", None, "Source")
    netapi.link(source, "gen", source, "gen")
    source.activation = 1
    nodenet.step()
    return nodenet, netapi, source


def test_node_logic_loop(test_nodenet):
    # test gen looping behaviour
    net, netapi, source = prepare(test_nodenet)
    net.step()
    assert source.get_gate("gen").activation == 1
    net.step()
    assert source.get_gate("gen").activation == 1
    netapi.link(source, "gen", source, "gen", 0.5)
    net.step()
    assert source.get_gate("gen").activation == 0.5


def test_node_logic_die(test_nodenet):
    # without the link, activation ought to drop to 0
    net, netapi, source = prepare(test_nodenet)

    netapi.unlink(source, "gen", source, "gen")
    net.step()
    assert source.get_gate("gen").activation == 0


def test_node_logic_sum(test_nodenet):
    # propagate positive activation, expect sum
    net, netapi, source = prepare(test_nodenet)

    reg_a = netapi.create_node("Register", None, "RegA")
    reg_b = netapi.create_node("Register", None, "RegB")
    reg_result = netapi.create_node("Register", None, "RegResult")

    netapi.link(source, "gen", reg_a, "gen", 0.5)
    netapi.link(source, "gen", reg_b, "gen", 0.5)
    netapi.link(reg_a, "gen", reg_result, "gen")
    netapi.link(reg_b, "gen", reg_result, "gen")

    net.step()
    net.step()
    assert reg_result.get_gate("gen").activation == 1


def test_node_logic_cancel(test_nodenet):
    # propagate positive and negative activation, expect cancellation
    net, netapi, source = prepare(test_nodenet)

    reg_a = netapi.create_node("Register", None, "RegA")
    reg_b = netapi.create_node("Register", None, "RegB")
    reg_b.set_gate_parameter("gen", "threshold", -100)
    reg_result = netapi.create_node("Register", None, "RegResult")

    netapi.link(source, "gen", reg_a, "gen", 1)
    netapi.link(source, "gen", reg_b, "gen", -1)
    netapi.link(reg_a, "gen", reg_result, "gen")
    netapi.link(reg_b, "gen", reg_result, "gen")

    net.step()
    net.step()
    assert reg_result.get_gate("gen").activation == 0


def test_node_logic_store_and_forward(test_nodenet):
    # collect activation in one node, go forward only if both dependencies are met
    net, netapi, source = prepare(test_nodenet)

    reg_a = netapi.create_node("Register", None, "RegA")
    reg_b = netapi.create_node("Register", None, "RegB")
    reg_b.set_gate_parameter("gen", "threshold", -100)
    reg_result = netapi.create_node("Register", None, "RegResult")
    reg_b.set_gate_parameter("gen", "threshold", 1)

    netapi.link(source, "gen", reg_a, "gen")
    netapi.link(reg_a, "gen", reg_result, "gen")
    netapi.link(reg_b, "gen", reg_result, "gen")
    net.step()
    assert reg_result.get_gate("gen").activation == 0

    netapi.link(source, "gen", reg_b, "gen")
    net.step()
    assert reg_result.get_gate("gen").activation == 1


def test_node_logic_activators(test_nodenet):
    net, netapi, source = prepare(test_nodenet)
    activator = netapi.create_node('Activator', None)
    activator.set_parameter('type', 'sub')
    activator.activation = 1

    testpipe = netapi.create_node("Pipe", None)
    netapi.link(source, "gen", testpipe, "sub", 0)
    net.step()
    net.step()
    assert testpipe.get_gate("sub").activation == 0


def test_node_logic_sensor(test_nodenet, default_world):
    # read a sensor value from the dummy world adapter
    net, netapi, source = prepare(test_nodenet)
    micropsi.set_nodenet_properties(test_nodenet, worldadapter="Default", world_uid=default_world)
    register = netapi.create_node("Register", None)
    netapi.link_sensor(register, "static_on", "gen")
    micropsi.step_nodenet(test_nodenet)
    micropsi.step_nodenet(test_nodenet)
    assert round(register.get_gate("gen").activation, 1) == 1


def test_node_logic_actor(test_nodenet, default_world):
    # write a value to the dummy world adapter
    net, netapi, source = prepare(test_nodenet)
    micropsi.set_nodenet_properties(test_nodenet, worldadapter="Default", world_uid=default_world)
    netapi.link_actor(source, "echo", weight=0.5, gate="gen")
    register = netapi.create_node("Register", None)
    actor = netapi.get_nodes(node_name_prefix="echo")[0]
    netapi.link(actor, "gen", register, "gen")
    micropsi.step_nodenet(test_nodenet)
    micropsi.step_nodenet(test_nodenet)
    micropsi.step_nodenet(test_nodenet)
    assert round(register.get_gate("gen").activation, 1) == 0.5
