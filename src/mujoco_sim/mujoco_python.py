import mujoco
from mujoco import viewer

xml_path = "ur5.mujoco.xml"

model = mujoco.MjModel.from_xml_path(xml_path)
data = mujoco.MjData(model)

with viewer.launch_passive(model, data) as v:
    while v.is_running():
        mujoco.mj_step(model, data)
