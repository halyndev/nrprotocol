# Copyright (c) 2026 Elmadani SALKA. 
"""
NRP Example: Multi-Node

Multi-node interaction example.
Registers 3 simulated sensors and reads their state.

    python examples/multi_node.py
"""

import asyncio
from nrp import NRPId, NRPManifest, ChannelSpec, ActionSpec, ShieldSpec
from nrp import NRPDriver, ShieldRule, ShieldType, EventBus, Severity


class FakeSensor(NRPDriver):
    """Simulated sensor for demo purposes."""

    def __init__(self, sensor_type: str = "temperature", value: float = 22.5):
        super().__init__()
        self.sensor_type = sensor_type
        self.value = value

    def manifest(self) -> NRPManifest:
        return NRPManifest(
            nrp_id=self._nrp_id or NRPId.create("demo", "sensor", self.sensor_type),
            manufacturer="Demo",
            model=f"{self.sensor_type.title()} Sensor",
            observe=[
                ChannelSpec(self.sensor_type, "float", unit="°C" if "temp" in self.sensor_type else "%"),
                ChannelSpec("battery", "int", unit="percent"),
            ],
            act=[
                ActionSpec("calibrate", {}, "Recalibrate sensor"),
                ActionSpec("set_threshold", {"value": "float"}, "Set alert threshold"),
            ],
            shield=[],
        )

    async def observe(self, channels=None):
        import random
        return {
            self.sensor_type: round(self.value + random.uniform(-2, 2), 1),
            "battery": 87,
        }

    async def act(self, command, args):
        if command == "calibrate":
            return {"status": "calibrated", "drift": 0.1}
        if command == "set_threshold":
            return {"threshold": args.get("value"), "status": "set"}
        return {"error": f"Unknown: {command}"}

    def shield_rules(self):
        return []


async def main():
    bus = EventBus()
    events = []
    bus.subscribe("*", lambda e: events.append(e))

    # Create 3 different nodes
    nodes = [
        ("nrp://farm/sensor/temp-north", FakeSensor("temperature", 24.0)),
        ("nrp://farm/sensor/moisture-east", FakeSensor("moisture", 35.0)),
        ("nrp://farm/sensor/ph-south", FakeSensor("ph", 6.8)),
    ]

    print("=== Multi-Node NRP Demo ===\n")

    for uri, driver in nodes:
        nrp_id = NRPId.parse(uri)
        driver.bind(nrp_id, bus)
        manifest = driver.manifest()
        print(f"{nrp_id.uri}")
        print(f"  Type: {manifest.model}")
        print(f"  Channels: {[c.name for c in manifest.observe]}")

        state = await driver.observe()
        for k, v in state.items():
            print(f"  {k} = {v}")
        print()

    # The AI would see all 3 nodes and their manifests
    # and could interact with all of them in one conversation:
    #
    #   "How is the farm?"
    #   → Temperature: 23.5°C (north), Moisture: 34.2% (east), pH: 6.9 (south)
    #     All nominal. Battery levels above 80%.
    #
    #   "The north field seems warm. Set temperature alert at 30°C"
    #   → Threshold set to 30°C on nrp://farm/sensor/temp-north
    #
    #   "Calibrate all sensors"
    #   → Calibrated 3 sensors. Max drift: 0.1

    print(f"Events captured: {len(events)}")
    print("\nThis is NRP. 3 nodes. 1 protocol. 1 conversation.")


if __name__ == "__main__":
    asyncio.run(main())

