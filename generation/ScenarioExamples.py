import OntologyGenerator as OG
from owlready2 import *

template_ontology = get_ontology('TemplateOntology.owl').load()

#为了实现场景结合，需要保证每个场景的主车初始位置和速度一致，用来防止结合产生冲突
bounding_box_object = OG.newBoundingBox("indiv", "-", 10, 10, 10, 10, 10, 10)
ego_init_speed = 5
ego_vehicle = template_ontology.ego_vehicle
ego_teleport_action = OG.newTeleportActionWithPosition(ego_vehicle, -1, 0, 0, 1, "indiv", "-")

def fallingSigns(n1, n2, filename):
    #Init
    transition_dynamics = OG.newTransitionDynamics(n1, n2, template_ontology.step, template_ontology.distance, 15)
    ego_speed_action_init = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "Ego_simple")
    streetsign1 = OG.newMisc(n1, n2 + "1", "static.prop.streetsign01")
    streetsign2 = OG.newMisc(n1, n2 + "2", "static.prop.streetsign01")
    streetsign3 = OG.newMisc(n1, n2 + "3", "static.prop.streetsign01")
    entities = [ego_vehicle, streetsign1, streetsign2, streetsign3]
    ss1_teleport_action = OG.newTeleportActionWithPosition(streetsign1, 2, 75, 0, 1, n1, n2 + "ss1_simple")
    ss2_teleport_action = OG.newTeleportActionWithPosition(streetsign2, -2, 70, 0, 1, n1, n2 + "ss2_simple")
    ss3_teleport_action = OG.newTeleportActionWithPosition(streetsign3, 2, 65, 0, 1, n1, n2 + "ss3_simple")
    environment_action = template_ontology.def_env_action
    init_actions = [ego_speed_action_init, ego_teleport_action, ss1_teleport_action, ss2_teleport_action, ss3_teleport_action, environment_action]
    init_scenario = OG.newInit(n1, n2, init_actions)

    # StartTrigger
    zero_sim_condition = OG.newSimulationCondition(0, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "zero_simple")
    condtion_group_zero = OG.newConditionGroup([zero_sim_condition], n1, n2 + "Zero_simple")
    start_trigger_zero = OG.newStartTrigger([condtion_group_zero], n1, n2 + "Zero_simple")

    # DistanceTrigger
    traveled_distance_condition = OG.newTraveledDistanceCondition(n1, n2 + "50_simple", ego_vehicle, 50, template_ontology.none)
    condition_group_distance = OG.newConditionGroup([traveled_distance_condition], n1, n2 + "Distance_simple")
    start_trigger_distance = OG.newStartTrigger([condition_group_distance], n1, n2 + "Distance_simple")

    # StopTrigger
    sim_condition_30 = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "30_simple")
    condtion_group_30 = OG.newConditionGroup([sim_condition_30], n1, n2 + "30_simple")
    stop_trigger_30 = OG.newStopTrigger([condtion_group_30], n1, n2 + "30_simple")

    # event1 sign倒下
    #ss1
    bbq_teleport_action_story = OG.newTeleportActionWithRelativePositionAndOrientation(n1, n2 + "ss1_simple", streetsign1, 0, 0, 0, 0.0, -0.5, 0)
    event1 = OG.newEvent([bbq_teleport_action_story], template_ontology.overwrite, start_trigger_distance, n1, n2 + "ss1_distance_simple")
    maneuver1 = OG.newManeuver([event1], n1, n2 + "ss1_simple")
    mg1 = OG.newManeuverGroup([maneuver1], streetsign1, n1, n2 + "ss1_simple")
    # ss2
    bbq_teleport_action_story2 = OG.newTeleportActionWithRelativePositionAndOrientation(n1, n2 + "ss2_simple", streetsign2, 0, 0, 0, 0.0, -0.5, 0)
    event2 = OG.newEvent([bbq_teleport_action_story2], template_ontology.overwrite, start_trigger_distance, n1, n2 + "ss2_distance_simple")
    maneuver2 = OG.newManeuver([event2], n1, n2 + "ss2_simple")
    mg2 = OG.newManeuverGroup([maneuver2], streetsign2, n1, n2 + "ss2_simple")
    #ss3
    bbq_teleport_action_story3 = OG.newTeleportActionWithRelativePositionAndOrientation(n1, n2 + "ss3_simple", streetsign3, 0, 0, 0, 0.0, -0.5, 0)
    event3 = OG.newEvent([bbq_teleport_action_story3], template_ontology.overwrite, start_trigger_distance, n1, n2 + "ss3_distance_simple")
    maneuver3 = OG.newManeuver([event3], n1, n2 + "ss3_simple")
    mg3 = OG.newManeuverGroup([maneuver3], streetsign3, n1, n2 + "ss3_simple")

    keep_longer_action = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "longer")

    storyboard_element_state_condition_event = OG.newStoryboardElementStateCondition(n1, n2 + "speedchange", template_ontology.completeState, event1, 0, template_ontology.none)
    condtion_group_complete_state = OG.newConditionGroup([storyboard_element_state_condition_event], n1, n2 + "completeState")
    start_trigger_state = OG.newStartTrigger([condtion_group_complete_state], n1, n2 + "StateTrigger")

    # event2 车辆保持原速行驶
    event_keep_longer = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_state, n1, n2 + "longer")

    longer_condition = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "longer")
    longer_group = OG.newConditionGroup([longer_condition], n1, n2 + "longer")
    start_trigger_longer = OG.newStartTrigger([longer_group], n1, n2 + "longer")

    # event3 状态继续保持一段时间
    event_complete = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_longer, n1, n2 + "complete")

    maneuver_vehicle = OG.newManeuver([event_keep_longer, event_complete], n1, n2)
    # maneuver_vehicle = OG.newManeuver([event_keep_longer], n1, n2)
    mg_vehicle = OG.newManeuverGroup([maneuver_vehicle], ego_vehicle, n1, n2)

    # Act and rest of the scenario
    scenario_act = OG.newAct([mg1, mg2, mg3, mg_vehicle], start_trigger_zero, stop_trigger_30, n1, n2 + "fallingsigns")
    story = OG.newStory([scenario_act], stop_trigger_30, n1, n2)
    storyboard = OG.newStoryboard(n1, n2, init_scenario, story)
    scenario = OG.newScenario(n1, n2, entities, storyboard, template_ontology.Town01)
    template_ontology.save(filename)
    return scenario

def intoFogOntology(n1, n2, filename):
    """
    Creates a Scenario individual, where the ego vehicle is driving, and after some time a dense fog appears.

    Parameters:

    n1,n2 - string used for the name of the individuals.

    filename - string used for the name of the scenario

    Returns the Scenario individual, with correct property assertions.
    """

    #Init
    transition_dynamics = OG.newTransitionDynamics(n1, n2, template_ontology.linear, template_ontology.distance, 15)
    ego_speed_action_init = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "Ego")
    init_weather = template_ontology.def_env_action
    init_actions = [ego_teleport_action, ego_speed_action_init, init_weather]
    init_scenario = OG.newInit(n1, n2, init_actions)

    # 定义Environment Action
    time_of_day = OG.newTimeOfDay(n1, n2 + "1200", "true", 2021, 1, 7, 13, 10, 10)
    road_condition = OG.newRoadCondition(n1, n2 + "1", 1)
    sun = OG.newSun(n1, n2, 1.3, 0, 0.8)
    bounding_box = OG.newBoundingBox(n1, n2 + "Fog_bb", 10, 10, 10, 10, 10, 10)
    fog = OG.newFog(n1, n2, 60, bounding_box)  #第三个参数是雾的浓度
    precipitation = OG.newPrecipitation(n1, n2 + "dry", 1, template_ontology.dry)
    weather = OG.newWeather(n1, n2 + "foggy", template_ontology.free, sun, fog, precipitation)
    environment = OG.newEnvironment(n1, n2, time_of_day, weather, road_condition)
    environment_action = OG.newEnvironmentAction(n1, n2 + "1", environment)

    # Start Triggers
    zero_sim_condition = OG.newSimulationCondition(0, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "zero")
    condtion_group_zero = OG.newConditionGroup([zero_sim_condition], n1, n2 + "Zero")
    start_trigger_zero = OG.newStartTrigger([condtion_group_zero], n1, n2 + "Zero")

    #stop triggers
    sim_condition_30 = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "30")
    condtion_group_30 = OG.newConditionGroup([sim_condition_30], n1, n2 + "30")
    stop_trigger_30 = OG.newStopTrigger([condtion_group_30], n1, n2 + "30")
    start_Trigger_30 = OG.newStartTrigger([condtion_group_30], n1, n2 + "30")

    #行驶50米后触发
    traveled_distance_condition = OG.newTraveledDistanceCondition(n1, n2 + "50", ego_vehicle, 50, template_ontology.none)
    condtion_group_distance = OG.newConditionGroup([traveled_distance_condition], n1, n2 + "Distance_intoFog")
    start_trigger_distance = OG.newStartTrigger([condtion_group_distance], n1, n2 + "Distance_intoFog")

    #event1 汽车行驶50米后环境变化，开始起雾
    event_weather_change = OG.newEvent([environment_action], template_ontology.overwrite, start_trigger_distance, n1, n2 + "weather_change")

    keep_longer_action = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "longer")

    condition_longer = OG.newStoryboardElementStateCondition(n1, n2 + "longer", template_ontology.completeState, event_weather_change, 0, template_ontology.none)
    condition_group = OG.newConditionGroup([condition_longer], n1, n2 + "longer")
    start_trigger_longer = OG.newStartTrigger([condition_group], n1, n2 + "longertrigger")

    #event2 汽车行驶一段时间
    event_keep_longer = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_longer, n1, n2 + "longer")

    #event3 汽车保持该状态一段时间
    event_complete = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_Trigger_30, n1, n2 + "complete")

    maneuver = OG.newManeuver([event_weather_change, event_keep_longer, event_complete], n1, n2)
    mg_vehicle = OG.newManeuverGroup([maneuver], ego_vehicle, n1, n2)

    scenario_act = OG.newAct([mg_vehicle], start_trigger_zero, stop_trigger_30, n1, n2)
    story = OG.newStory([scenario_act], stop_trigger_30, n1, n2)
    storyboard = OG.newStoryboard(n1, n2, init_scenario, story)
    scenario = OG.newScenario(n1, n2, [ego_vehicle], storyboard, template_ontology.Town01)

    print("done environment")
    template_ontology.save(filename)
    return scenario

def ManyPedestriansOntology(n1, n2, filename):
    """
    Creates a Scenario individual, where the ego vehicle is driving behind "n" amount of pedestrians. After some time, the pedestrians start running.

    Parameters:

    n1,n2 - string used for the name of the individuals.

    filename - string used for the name of the scenario

    Returns the Scenario individual, with correct property assertions.
    """

    #Init
    transition_dynamics = OG.newTransitionDynamics(n1, n2, template_ontology.step, template_ontology.distance, 15)
    scenarioTown = template_ontology.Town01
    amountPedestrians = 10
    #scenario的定义由最后位置提前到此位置
    newScenario = template_ontology.Scenario(n1 + n2 + "Scenario")
    newStoryboard = template_ontology.Storyboard(n1 + n2 + "Storyboard")
    newScenario.has_storyboard.append(newStoryboard)   #storyboard
    newScenario.has_town.append(scenarioTown)  #network
    # entities
    pedestrian_assets = OG.getPedestrianAssets()
    for i in range(amountPedestrians):
        ped = OG.newPedestrian(n1, str(i), pedestrian_assets[i], bounding_box_object)
        newScenario.has_entity.append(ped)

    # story
    story = template_ontology.Story(n1 + n2 + "Story")
    newStoryboard.has_story.append(story)

    newScenario.has_entity.append(ego_vehicle)
    # init
    new_init = template_ontology.Init(n1 + n2 + "Init")
    # Ego Vehicle Actions
    actionSpeedEgo = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "EgoSpeed")
    new_init.has_init_action.append(actionSpeedEgo)
    new_init.has_init_action.append(ego_teleport_action)
    weatheraction = template_ontology.def_env_action
    new_init.has_init_action.append(weatheraction)
    newStoryboard.has_init.append(new_init)
    maneuver_groups = []
    # Add amountPedestrians pedestrians in the ontology
    s_jump = 20
    for i in range(amountPedestrians):
        actions = []
        events = []
        # place = 5
        pedestrian_assets = OG.getPedestrianAssets()
        pedestrian = OG.newPedestrian(n1, str(i), pedestrian_assets[i], bounding_box_object)
        #行人交叉放置
        if i % 2 == 0:
            offset = -1
        else:
            offset = 0
        actionTeleport = OG.newTeleportActionWithPosition(pedestrian, -1, s_jump, offset, 1, n1, str(i))
        actionSpeed = OG.newSpeedAction(pedestrian, 4, transition_dynamics, n1, str(i))
        new_init.has_init_action.append(actionTeleport)
        new_init.has_init_action.append(actionSpeed)
        speed_action = OG.newSpeedAction(pedestrian, 8, transition_dynamics, n1 + "_0_", str(i))
        # actions.append(action3)
        zero_sim_condition = OG.newSimulationCondition(3, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "zero")
        condition_group_zero = OG.newConditionGroup([zero_sim_condition], n1, n2 + "Zero")
        start_trigger_zero = OG.newStartTrigger([condition_group_zero], n1, n2 + "Zero")

        #event1 行人加速
        event1 = OG.newEvent([speed_action], template_ontology.overwrite, start_trigger_zero, n1, str(i))
        events.append(event1)
        maneuver_ped = OG.newManeuver(events, n1, str(i))
        mg_ped = OG.newManeuverGroup([maneuver_ped], pedestrian, n1, str(i))
        maneuver_groups.append(mg_ped)

        keep_longer_action = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "longer")

        accelerate_condition = OG.newStoryboardElementStateCondition(n1, n2 + "longer", template_ontology.completeState, event1, 0, template_ontology.none)
        condition_group_accelerate = OG.newConditionGroup([accelerate_condition], n1, n2 + "longer")
        start_trigger_accelerate = OG.newStartTrigger([condition_group_accelerate], n1, n2 + "longer")

        #event2 汽车原速行驶
        event_longer = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_accelerate, n1, n2 + "longer")

        keep_longer = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "complete")
        condition_group_keep = OG.newConditionGroup([keep_longer], n1, n2 + "complete")
        start_trigger_keep = OG.newStartTrigger([condition_group_keep], n1, n2 + "complete")

        #event3 让汽车状态保持一段时间
        event_complete = OG.newEvent([actionSpeed], template_ontology.overwrite, start_trigger_keep, n1, n2 + "complete")

        maneuver_ego_vehicle = OG.newManeuver([event_longer, event_complete], n1, n2)
        mg_ego_vehicle = OG.newManeuverGroup([maneuver_ego_vehicle], ego_vehicle, n1, n2)
        maneuver_groups.append(mg_ego_vehicle)

        s_jump += 4

    #Start Trigger
    zero_sim_condition = OG.newSimulationCondition(0, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "zero")
    condtion_group_zero = OG.newConditionGroup([zero_sim_condition], n1, n2 + "Zero")
    start_trigger_zero = OG.newStartTrigger([condtion_group_zero], n1, n2 + "Zero")

    #StopTrigger
    sim_condition_30 = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "30")
    condtion_group_30 = OG.newConditionGroup([sim_condition_30], n1, n2 + "30")
    stop_trigger_30 = OG.newStopTrigger([condtion_group_30], n1, n2 + "30")

    act = OG.newAct(maneuver_groups, start_trigger_zero, stop_trigger_30, n1, n2)
    story.has_act.append(act)
    template_ontology.save(filename)
    return newScenario

def BicycleOnOneWheelOntology(n1, n2, filename):
    """
    Creates a Scenario individual, where the ego vehicle is just driving and in the opposite lane, a cyclist starts executing strange manuevers.

    Parameters:

    n1,n2 - string used for the name of the individuals.

    filename - string used for the name of the scenario

    Returns the Scenario individual, with correct property assertions.
    """

    #Init
    bicycle_speed = 8
    transition_dynamics = OG.newTransitionDynamics(n1, n2, template_ontology.step, template_ontology.distance, 15)
    bicycle = OG.newBicycle(n1, n2 + "bicycle", OG.getBicycleAssets()[0], bounding_box_object)
    entities = [ego_vehicle, bicycle]
    ego_speed_action_init = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "Ego")
    bike_speed_action_init = OG.newSpeedAction(bicycle, bicycle_speed, transition_dynamics, n1, n2 + "bicycle")
    # ego_teleport_action = OG.newTeleportActionWithPosition(ego_vehicle, -1, 0, 0, 1, n1, n2 + "Ego")
    bike_teleport_action = OG.newTeleportActionWithPosition(bicycle, 1, 80, 0, 1, n1, n2 + "bicycle")
    environment_action = template_ontology.def_env_action
    init_actions = [ego_speed_action_init, bike_speed_action_init, ego_teleport_action, bike_teleport_action, environment_action]
    init_scenario = OG.newInit(n1, n2, init_actions)

    # Triggers
    zero_sim_condition = OG.newSimulationCondition(0, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "zero")
    condtion_group_zero = OG.newConditionGroup([zero_sim_condition], n1, n2 + "Zero")
    start_trigger_zero = OG.newStartTrigger([condtion_group_zero], n1, n2 + "Zero")

    #行驶30米后触发
    traveled_distance_condition = OG.newTraveledDistanceCondition(n1, n2 + "30", bicycle, 30, template_ontology.rising)
    traveled_condition_group = OG.newConditionGroup([traveled_distance_condition], n1, n2 + "travel")
    start_trigger_distance = OG.newStartTrigger([traveled_condition_group], n1, n2 + "travel")

    # StopTrigger
    sim_condition_30 = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "30")
    condtion_group_30 = OG.newConditionGroup([sim_condition_30], n1, n2 + "30")
    stop_trigger_30 = OG.newStopTrigger([condtion_group_30], n1, n2 + "30")

    # 定义自行车奇怪的动作，相对于初始位置的偏移
    bicycle_teleport_action_story = OG.newTeleportActionWithRelativePositionAndOrientation(n1, n2 + "bicycle", bicycle, 0, 0, 0.7, 0.7, 0, 0.7)

    #event1 自行车行驶30米后开始奇怪的行为
    event1 = OG.newEvent([bicycle_teleport_action_story], template_ontology.overwrite, start_trigger_distance, n1, n2 + "bicycle_onwheel")
    #定义bicycle的maneuver
    maneuver_bicycle = OG.newManeuver([event1], n1, n2 + "bicycle_onwheel")
    mg_bicycle = OG.newManeuverGroup([maneuver_bicycle], bicycle, n1, n2 + "bicycle_onwheel")

    keep_longer_action = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "longer")

    storyboard_element_state_condition_event1 = OG.newStoryboardElementStateCondition(n1, n2 + "speedchange", template_ontology.completeState, event1, 0, template_ontology.none)
    condition_group_complete_state = OG.newConditionGroup([storyboard_element_state_condition_event1], n1, n2 + "completeState")
    start_trigger_state = OG.newStartTrigger([condition_group_complete_state], n1, n2 + "StateTrigger")

    #event2 汽车保持原速行驶
    event_keep_longer = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_state, n1, n2 + "longer")

    keep_time_condition = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "keeptime_onwheel")
    condition_group_keeptime = OG.newConditionGroup([keep_time_condition], n1, n2 + "keeptime_onwheel")
    start_trigger_time = OG.newStartTrigger([condition_group_keeptime], n1, n2 + "keeptime_onwheel")

    # event3 该状态保持一定时间
    keep_complete = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_time, n1, n2 + "complete")

    #统一定义ego_vehicle的maneuver
    maneuver_ego_vehicle = OG.newManeuver([event_keep_longer, keep_complete], n1, n2)
    mg_ego_vehicle = OG.newManeuverGroup([maneuver_ego_vehicle], ego_vehicle, n1, n2)

    # rest
    scenario_act = OG.newAct([mg_bicycle, mg_ego_vehicle], start_trigger_zero, stop_trigger_30, n1, n2 + "onwheel")
    story = OG.newStory([scenario_act], stop_trigger_30, n1, n2)
    storyboard = OG.newStoryboard(n1, n2, init_scenario, story)
    scenario = OG.newScenario(n1, n2, entities, storyboard, template_ontology.Town01)
    template_ontology.save(filename)
    return scenario

def randomObjectOntology(n1, n2, filename):
    """
    Creates a Scenario individual, where the ego vehicle is driving and suddenly an unknown objects appears, that falls very close to the ego vehicle.
    Parameters:

    n1,n2 - string used for the name of the individuals.

    filename - string used for the name of the scenario

    Returns the Scenario individual, with correct property assertions.
    """

    #Init
    transition_dynamics = OG.newTransitionDynamics(n1, n2, template_ontology.step, template_ontology.distance, 15)
    ego_speed_action_init = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "Ego")
    barbeque = OG.newMisc(n1, n2, "static.prop.vendingmachine")
    entities = [ego_vehicle, barbeque]
    barbeque_teleport_action_init = OG.newTeleportActionWithPosition(barbeque, 1, 65, -1, 1, n1, n2 + "bbq_randomObject")
    environment_action = template_ontology.def_env_action
    init_actions = [ego_speed_action_init, ego_teleport_action, barbeque_teleport_action_init, environment_action]
    init_scenario = OG.newInit(n1, n2, init_actions)

    # StartTrigger
    zero_sim_condition = OG.newSimulationCondition(0, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "zero")
    condition_group_zero = OG.newConditionGroup([zero_sim_condition], n1, n2 + "Zero")
    start_trigger_zero = OG.newStartTrigger([condition_group_zero], n1, n2 + "Zero")

    # DistanceTrigger 汽车行驶多远以后自动售卖机倒下
    traveled_distance_condition = OG.newTraveledDistanceCondition(n1, n2 + "50", ego_vehicle, 50, template_ontology.none)
    condition_group_distance = OG.newConditionGroup([traveled_distance_condition], n1, n2 + "Distance_randomObject")
    start_trigger_distance = OG.newStartTrigger([condition_group_distance], n1, n2 + "Distance_randomObject")

    # StopTrigger
    sim_condition_30 = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "30")
    condition_group_30 = OG.newConditionGroup([sim_condition_30], n1, n2 + "30")
    stop_trigger_30 = OG.newStopTrigger([condition_group_30], n1, n2 + "30")

    # bbq teleport action 倒下方向和位置
    bbq_teleport_action_story = OG.newTeleportActionWithRelativePositionAndOrientation(n1, n2, barbeque, 0, 0, 0, 0, -0.5, 0)

    #event1 自动售卖机倒下
    event1 = OG.newEvent([bbq_teleport_action_story], template_ontology.overwrite, start_trigger_distance, n1, n2 + "bbq_randomObject")

    #定义售卖机的maneuver
    maneuver_barbeque = OG.newManeuver([event1], n1, n2 + "bbq_randomObject")
    mg_barbeque = OG.newManeuverGroup([maneuver_barbeque], barbeque, n1, n2 + "bbq_randomObject")

    # ego speed
    keep_longer_action = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "longer")

    #delay是自动售卖机倒下事件多久之后发生
    storyboard_element_state_condition_event1 = OG.newStoryboardElementStateCondition(n1, n2 + "speedchange", template_ontology.completeState, event1, 0, template_ontology.none)
    condtion_group_complete_state = OG.newConditionGroup([storyboard_element_state_condition_event1], n1, n2 + "completeState")
    start_trigger_state = OG.newStartTrigger([condtion_group_complete_state], n1, n2 + "StateTrigger")

    #event2 售卖机倒下后 汽车原速行驶
    event_keep_longer = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_state, n1, n2 + "longer")

    start_trigger_longer = OG.newStartTrigger([condition_group_30], n1, n2 + "30")

    #event3 保持该状态一段时间
    event_complete = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_longer, n1, n2 + "complete")

    #统一定义ego_vehicle的maneuver
    maneuver_ego_vehicle = OG.newManeuver([event_keep_longer, event_complete], n1, n2)
    mg_ego_vehicle = OG.newManeuverGroup([maneuver_ego_vehicle], ego_vehicle, n1, n2)

    # Act and rest of the scenario
    scenario_act = OG.newAct([mg_barbeque, mg_ego_vehicle], start_trigger_zero, stop_trigger_30, n1, n2 + "randomobject")
    story = OG.newStory([scenario_act], stop_trigger_30, n1, n2)
    storyboard = OG.newStoryboard(n1, n2, init_scenario, story)
    scenario = OG.newScenario(n1, n2, entities, storyboard, template_ontology.Town01)
    template_ontology.save(filename)
    return scenario

def suddenlyAppeared(n1, n2, filename):
    """
    Creates a Scenario individual, where the ego vehicle is driving and a pedestrian suddenly runs in front of the ego vehicle.

    Parameters:

    n1,n2 - string used for the name of the individuals.

    filename - string used for the name of the scenario

    Returns the Scenario individual, with correct property assertions.
    """

    #Init
    transition_dynamics = OG.newTransitionDynamics(n1, n2, template_ontology.step, template_ontology.distance, 15)
    pedestrian = OG.newPedestrian(n1, n2 + "pedestrian", OG.getPedestrianAssets()[0], bounding_box_object)
    barbeque = OG.newMisc(n1, n2, "static.prop.vendingmachine")
    entities = [ego_vehicle, pedestrian, barbeque]
    ped_teleport_action = OG.newTeleportActionWithPosition(pedestrian, 2, 40, -10, 1, n1, n2 + "pedestrian")
    barbeque_teleport_action = OG.newTeleportActionWithPosition(barbeque, 2, 39, -10, 1, n1, n2 + "bbq_init")
    ego_speed_action_init = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "Ego")
    weather_action = template_ontology.def_env_action
    init_actions = [ego_teleport_action, ped_teleport_action, barbeque_teleport_action, ego_speed_action_init, weather_action]
    init_scenario = OG.newInit(n1, n2, init_actions)

    # triggers
    zero_sim_condition = OG.newSimulationCondition(0, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "zero")
    condtion_group_zero = OG.newConditionGroup([zero_sim_condition], n1, n2 + "Zero")
    start_trigger_zero = OG.newStartTrigger([condtion_group_zero], n1, n2 + "Zero")

    #行人距离车辆多远跑过来
    relative_distance_condition = OG.newRelativeDistanceCondition(n1, n2, 17, template_ontology.lessThan, template_ontology.cartesianDistance, template_ontology.ego_vehicle, pedestrian, 0, template_ontology.rising)
    condition_group_distance = OG.newConditionGroup([relative_distance_condition], n1, n2 + "Distance")
    start_trigger_distance = OG.newStartTrigger([condition_group_distance], n1, n2 + "DistanceTrigger")

    # StopTrigger
    sim_condition_30 = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "30")
    condtion_group_30 = OG.newConditionGroup([sim_condition_30], n1, n2 + "30")
    stop_trigger_30 = OG.newStopTrigger([condtion_group_30], n1, n2 + "30")

    start_trigger_30 = OG.newStartTrigger([condtion_group_30], n1, n2 + "30")

    # Start running event
    pedestrian_teleport_action_story = OG.newTeleportActionWithRelativePositionAndOrientation(n1, n2 + "ss1", pedestrian, 0, 0, 0, 0, 0, -1.5)
    pedestrian_speed_action = OG.newSpeedAction(pedestrian, 7, transition_dynamics, n1, n2 + "pedestrian")

    #event1 行人突然冲到车前面
    event1 = OG.newEvent([pedestrian_teleport_action_story, pedestrian_speed_action], template_ontology.overwrite, start_trigger_distance, n1, n2 + "bbq_distance")

    #定义行人的maneuver
    maneuver_ped = OG.newManeuver([event1], n1, n2 + "pedestrian1")
    mg_ped = OG.newManeuverGroup([maneuver_ped], pedestrian, n1, n2 + "pedestrian2")

    # keeplonger
    keep_longer_action = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "longer")
    # stop_action = OG.newSpeedAction(ego_vehicle, 0, transition_dynamics, n1, n2 + "stop")

    storyboard_element_state_condition_event1 = OG.newStoryboardElementStateCondition(n1, n2 + "speedchange", template_ontology.completeState, event1, 0, template_ontology.none)
    condtion_group_complete_state = OG.newConditionGroup([storyboard_element_state_condition_event1], n1, n2 + "completeState")
    start_trigger_state = OG.newStartTrigger([condtion_group_complete_state], n1, n2 + "StateTrigger")

    #event2 车保持原速行驶
    event_keep_longer = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_state, n1, n2 + "longer")

    #event3 速度为0的状态保持一段时间
    keep_complete = OG.newEvent([keep_longer_action], template_ontology.overwrite, start_trigger_30, n1, n2 + "complete")

    #统一定义ego_vehicle的maneuver
    maneuver_ego_vehicle = OG.newManeuver([event_keep_longer, keep_complete], n1, n2)
    mg_ego_vehicle = OG.newManeuverGroup([maneuver_ego_vehicle], ego_vehicle, n1, n2)

    #定义scenario
    scenario_act = OG.newAct([mg_ped, mg_ego_vehicle], start_trigger_zero, stop_trigger_30, n1, n2 + "suddenly_appeared")
    story = OG.newStory([scenario_act], stop_trigger_30, n1, n2)
    storyboard = OG.newStoryboard(n1, n2, init_scenario, story)
    scenario = OG.newScenario(n1, n2, entities, storyboard, template_ontology.Town01)
    template_ontology.save(filename)
    return scenario

def runningIntoCar(n1, n2, filename):
    #Init
    transition_dynamics = OG.newTransitionDynamics(n1, n2, template_ontology.step, template_ontology.distance, 15)
    pedestrian_simple = OG.newPedestrian(n1, n2 + "pedestrian_simple", OG.getPedestrianAssets()[0], bounding_box_object)
    entities = [ego_vehicle, pedestrian_simple]
    ped_teleport_action = OG.newTeleportActionWithPosition(pedestrian_simple, 2, 40, 2, 1, n1, n2 + "pedestrian_simple")
    ego_speed_action_init = OG.newSpeedAction(ego_vehicle, ego_init_speed, transition_dynamics, n1, n2 + "Ego_simple")
    weather_action = template_ontology.def_env_action
    init_actions = [ego_teleport_action, ped_teleport_action, ego_speed_action_init, weather_action]
    init_scenario = OG.newInit(n1, n2, init_actions)

    # triggers
    zero_sim_condition = OG.newSimulationCondition(0, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "zero_simple")
    condtion_group_zero = OG.newConditionGroup([zero_sim_condition], n1, n2 + "Zero_simple")
    start_trigger_zero = OG.newStartTrigger([condtion_group_zero], n1, n2 + "Zero_simple")

    #行人距离车辆多远跑过来
    relative_distance_condition = OG.newRelativeDistanceCondition(n1, n2, 17, template_ontology.lessThan, template_ontology.cartesianDistance, template_ontology.ego_vehicle, pedestrian_simple, 0, template_ontology.rising)
    condition_group_distance = OG.newConditionGroup([relative_distance_condition], n1, n2 + "Distance_simple")
    start_trigger_distance = OG.newStartTrigger([condition_group_distance], n1, n2 + "DistanceTrigger_simple")

    # StopTrigger
    sim_condition_30 = OG.newSimulationCondition(30, 0, template_ontology.rising, template_ontology.greaterThan, n1, n2 + "30_simple")
    condtion_group_30 = OG.newConditionGroup([sim_condition_30], n1, n2 + "30_simple")
    stop_trigger_30 = OG.newStopTrigger([condtion_group_30], n1, n2 + "30_simple")

    # Start running event
    pedestrian_teleport_action_story = OG.newTeleportActionWithRelativePositionAndOrientation(n1, n2 + "ss1_simple", pedestrian_simple, 0, 0, 0, 0, 0, 1.5)
    pedestrian_speed_action = OG.newSpeedAction(pedestrian_simple, 7, transition_dynamics, n1, n2 + "pedestrian_simple")

    #event1 行人突然冲到车前面
    event1 = OG.newEvent([pedestrian_teleport_action_story, pedestrian_speed_action], template_ontology.overwrite, start_trigger_distance, n1, n2 + "bbq_distance_simple")

    #定义行人的maneuver
    maneuver_ped = OG.newManeuver([event1], n1, n2 + "pedestrian_simple")
    mg_ped = OG.newManeuverGroup([maneuver_ped], pedestrian_simple, n1, n2 + "pedestrian_simple")

    scenario_act = OG.newAct([mg_ped], start_trigger_zero, stop_trigger_30, n1, n2 + "1_simple")
    story = OG.newStory([scenario_act], stop_trigger_30, n1, n2)
    storyboard = OG.newStoryboard(n1, n2, init_scenario, story)
    scenario = OG.newScenario(n1, n2, entities, storyboard, template_ontology.Town01)
    template_ontology.save(filename)
    return scenario


def main():
    current_time = time.localtime()

    #Fog
    # filename_into_fog = f'domain_shift_{current_time.tm_hour}_{current_time.tm_min}_{current_time.tm_sec}.owl'
    # intoFogOntology("indiv","_",filename_into_fog)
    # print("Executing Onto2OpenSCENARIO.py:")
    # os.system("python3 Onto2OpenSCENARIO.py " + filename_into_fog)


    # #ManyPedestrians
    # filename_many_ped = f'collective_anomaly_{current_time.tm_hour}_{current_time.tm_min}_{current_time.tm_sec}.owl'
    # ManyPedestriansOntology("indiv", "_", filename_many_ped)
    # print("Executing Onto2OpenSCENARIO.py:")
    # os.system("python3 Onto2OpenSCENARIO.py " + filename_many_ped)


    #COCACOLA
    # filename_cola = f'single_point_anomaly_{current_time.tm_hour}_{current_time.tm_min}_{current_time.tm_sec}.owl'
    # randomObjectOntology("indiv", "_", filename_cola)
    # print("Executing Onto2OpenSCENARIO.py:")
    # os.system("python3 Onto2OpenSCENARIO.py " + filename_cola)

    #STREET SIGNS
    # filename_ss = f'novel_scenario_{current_time.tm_hour}_{current_time.tm_min}_{current_time.tm_sec}.owl'
    # fallingSigns("indiv","_",filename_ss)
    # print("Executing Onto2OpenSCENARIO.py:")
    # os.system("python3 Onto2OpenSCENARIO.py " + filename_ss)

    # #Bicycle
    # filename_ss = f'anomalous_scenario{current_time.tm_hour}_{current_time.tm_min}_{current_time.tm_sec}.owl'
    # BicycleOnOneWheelOntology("indiv","_",filename_ss)
    # print("Executing Onto2OpenSCENARIO.py:")
    # os.system("python3 Onto2OpenSCENARIO.py " + filename_ss)

    #running into car
    # filename_ss = f'risky_scenario_running_into_car{current_time.tm_hour}_{current_time.tm_min}_{current_time.tm_sec}.owl'
    # runningIntoCar("indiv","_",filename_ss)
    # print("Executing Onto2OpenSCENARIO.py:")
    # os.system("python3 Onto2OpenSCENARIO.py " + filename_ss)

    #suddenly appeared
    filename_suddenly = f'risky_scenario_suddenly_appeared{current_time.tm_hour}_{current_time.tm_min}_{current_time.tm_sec}.owl'
    suddenlyAppeared("indiv", "_", filename_suddenly)
    print("Executing Onto2OpenSCENARIO.py:")
    os.system("python3 Onto2OpenSCENARIO.py " + filename_suddenly)

if __name__ == "__main__":
        main()
        print("done")
