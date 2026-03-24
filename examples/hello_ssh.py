# Copyright (c) 2026 Elmadani SALKA. 
"""
NRP Example: Hello World

Connect to a server via SSH and read its state.
This is the simplest possible NRP interaction.

    python examples/hello_ssh.py
"""

import asyncio
from nrp import NRPId, NRPDriver, NRPManifest, ChannelSpec, ActionSpec, ShieldSpec, ShieldRule, ShieldType, EventBus


class SimpleSSH(NRPDriver):
    """Minimal SSH driver — 60 lines."""

    def __init__(self, host: str, user: str = "root"):
        super().__init__()
        self.host = host
        self.user = user

    def manifest(self) -> NRPManifest:
        return NRPManifest(
            nrp_id=self._nrp_id or NRPId.create("local", "server", self.host),
            manufacturer="Linux",
            model="Server",
            observe=[
                ChannelSpec("hostname", "string"),
                ChannelSpec("uptime", "string"),
                ChannelSpec("load", "string"),
            ],
            act=[
                ActionSpec("shell", {"command": "string"}, "Run shell command", dangerous=True),
            ],
            shield=[
                ShieldSpec("no_rm_rf", "pattern", "rm -rf"),
            ],
        )

    async def observe(self, channels=None):
        import subprocess
        target = f"{self.user}@{self.host}"
        commands = {"hostname": "hostname", "uptime": "uptime -p", "load": "cat /proc/loadavg"}
        result = {}
        for ch in (channels or commands.keys()):
            if ch in commands:
                r = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", target, commands[ch]],
                                   capture_output=True, text=True, timeout=10)
                result[ch] = r.stdout.strip()
        return result

    async def act(self, command, args):
        import subprocess
        if command == "shell":
            r = subprocess.run(
                ["ssh", "-o", "StrictHostKeyChecking=no", f"{self.user}@{self.host}", args["command"]],
                capture_output=True, text=True, timeout=30,
            )
            return r.stdout
        return f"Unknown command: {command}"

    def shield_rules(self):
        return [ShieldRule("no_rm_rf", ShieldType.PATTERN, "rm -rf")]


async def main():
    # 1. Create identity
    nrp_id = NRPId.parse("nrp://local/server/my-server")
    print(f"Identity: {nrp_id.uri}")

    # 2. Create driver
    driver = SimpleSSH(host="localhost")

    # 3. Bind to event bus
    bus = EventBus()
    driver.bind(nrp_id, bus)

    # 4. Read manifest
    manifest = driver.manifest()
    print(f"\nManifest:")
    print(manifest.to_llm_description())

    # 5. Observe
    print(f"\nObserving...")
    state = await driver.observe()
    for k, v in state.items():
        print(f"  {k}: {v}")

    print(f"\nDone. This node is now AI-ready.")


if __name__ == "__main__":
    asyncio.run(main())

