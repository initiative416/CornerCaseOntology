# 基于本体的正向安全关键仿真测试场景生成代码说明

## 1.代码结构

```
├── README.md
├── Steps_add_animals # 在carla中添加新资产的步骤
├── generation # 存放所有信息的主文件
  ├── Onto2OpenSCENARIO.py # 将本体owl格式文件转为OpenSCENARIO格式文件
  ├── OntologyGenerator.py # 读取主本体模板文件，依据此创建具有相同结构和个体的新本体
  ├── ScenarioExamples.py # 创建corner case特定场景示例
  ├── TemplateOntology.owl # 主本体模板文件
  ├── Videos # 场景录像
  ├── __pycache__
  ├── carla_get_data.py # 在scenario_runner运行时结合使用，读取主车获取的信息
  ├── newScenarios # 存放OpenSCENARIO文件
```

代码的主要部分是这四个文件：Onto2OpenSCENARIO.py，OntologyGenerator.py，ScenarioExamples.py和TemplateOntology.owl。其中

1. ScenarioExamples.py：主要提供特定场景示例，此文件也是程序运行入口
2. TemplateOntology.owl：作为要创建所有场景主体的模板，owl文件可以利用[Protégé](https://protege.stanford.edu/)进行查看和修改
3. OntologyGenerator.py：在主本体TemplateOntology.owl基础上，利用此脚本创建和描述一个新的特定场景本体
4. Onto2OpenSCENARIO.py：读取创建好的本体owl文件，以生成carla的scenario runner内部模拟所需要的OpenSCENARIO文件

## 2.环境安装

### 1.版本

python>=3.7

[carla==0.9.13](https://mirrors.sustech.edu.cn/carla/)

[Scenario Runner==0.9.13（和carla版本保持一致）](https://link.zhihu.com/?target=https%3A//github.com/carla-simulator/scenario_runner/releases)

### 2.Scenario Runner安装

1. 需要下载和carla版本一致的[Scenario Runner(SR)](https://link.zhihu.com/?target=https%3A//github.com/carla-simulator/scenario_runner/releases)

2. 安装依赖：建议使用conda环境

   ```
   cd xxx/scenario_runner-0.9.13
   
   #Python 3.x
   sudo apt remove python3-networkx #if installed, remove old version of networkx
   pip3 install --user -r requirements.txt
   ```

3. 添加环境变量

   ```
   #carla 0.9.13
   export CARLA_ROOT=/path/to/your/carla/installation
   export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg:${CARLA_ROOT}/PythonAPI/carla/agents:${CARLA_ROOT}/PythonAPI/carla
   export SCENARIO_RUNNER_PATH=/path/to/your/scenario_runner/installation
   ```

4. 测试安装是否成功

   ```python
   ./CarlaUE4.sh
   
   python scenario_runner.py --scenario FollowLeadingVehicle_1 --reloadWorld
   python manual_control.py
   ```

## 3.运行步骤

### 1.单个场景生成

1. 运行ScenarioExample.py文件，生成特定场景的本体owl文件，xodr文件和xosc文件

2. 利用Scenario Runner运行xosc文件

   ```
   ./CarlaUE4.sh
   
   cd xxx/scenario_runner-0.9.13
   python3 scenario_runner.py --openscenario xxx/generation/newScenarios/xosc/xxx.xosc
   ```

### 2.结合场景生成

1. 通过对单个场景的生成，有各corner case场景的owl文件

2. 利用Onto2OpenSCENARIO.py文件对任意多个owl文件进行结合，生成多个场景结合后的场景

   ```
   ./CarlaUE4.sh
   cd xxx/generation
   python3 Onto2OpenSCENARIO.py 1.owl 2.owl ...  #会生成场景结合后的xosc文件
   
   cd xxx/scenario_runner-0.9.13
   python3 scenario_runnner.py --openscenario xxx/generation/newScenarios/xosc/xxx.xosc #运行场景结合后的xosc文件
   ```

## 4.构建场景示例

![image-20230404170753050](/home/lulu/.config/Typora/typora-user-images/image-20230404170753050.png)

## 5.要点

在使用本体创建新场景时，注意使用"n1"和"n2"参数为新个体指定不同的名称，如果两个变量在本体中具有相同的名称，则可能会导致冲突的发生。因此，在不同特定场景构建过程中，除主车外需要对其他实体及属性的名称进行区分，这样即可实现不同场景之间的任意结合，避免出现场景中实体或行为的冲突。

## 6.代码改进内容

1. 对原代码进行了整理和简化，统一各场景示例的代码逻辑
2. 对主车的行为，初始位置和初始速度进行了统一，对实体及属性命名进行了修改，以保证场景结合不会发生冲突
3. 对整个场景的运行进行了完善，原代码中场景在最后一个event结束后立即结束，修改后变为主车完成所有event并且场景经过30秒后，整个场景才结束
4. corner case中增加“鬼探头”场景，即主车行驶时，行人在自动售卖机后突然驶入主车前
5. 实现了对多个场景的结合生成新的场景功能，原代码是手动对不同类别的corner case进行结合，修改后的代码可以实现基于owl文件实现任意多个场景的结合