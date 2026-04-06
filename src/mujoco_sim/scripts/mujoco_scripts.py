import mujoco
from mujoco import viewer

xml_path = "/home/nithish/ROS/waste_ws/src/robot_description/urdf/ur5.mujoco.xml"

model = mujoco.MjModel.from_xml_path(xml_path)
data = mujoco.MjData(model)

qpos = data.qpos
qvel = data.qvel

joint_names = []
joint_positions = []

for i in range(model.njnt):
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
    
    if model.jnt_type[i] == mujoco.mjtJoint.mjJNT_HINGE:
        joint_names.append(name)
        joint_positions.append(data.qpos[model.jnt_qposadr[i]])

        
with viewer.launch_passive(model, data) as v:
    while v.is_running():
        mujoco.mj_step(model, data)