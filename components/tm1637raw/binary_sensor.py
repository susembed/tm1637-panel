import esphome.codegen as cg
from esphome.components import binary_sensor
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_KEY

CONF_TM1637_ID = "tm1637_id"

tm1637raw_ns = cg.esphome_ns.namespace("tm1637raw")
TM1637RawDisplay = tm1637raw_ns.class_("TM1637RawDisplay", cg.PollingComponent)
TM1637RawKey = tm1637raw_ns.class_("TM1637RawKey", binary_sensor.BinarySensor)

CONFIG_SCHEMA = binary_sensor.binary_sensor_schema(TM1637RawKey).extend(
    {
        cv.GenerateID(CONF_TM1637_ID): cv.use_id(TM1637RawDisplay),
        cv.Required(CONF_KEY): cv.int_range(min=0, max=15),
    }
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await binary_sensor.register_binary_sensor(var, config)
    cg.add(var.set_keycode(config[CONF_KEY]))
    hub = await cg.get_variable(config[CONF_TM1637_ID])
    cg.add(hub.add_tm1637_key(var))
