import json

import frida

device = frida.get_usb_device()

process_list = """
com.cyjh.gundam
com.cyjh.gundam.service.ScriptService.p
com.cyjh.gundam:mqrun
""".strip().splitlines()

for process in process_list:
    session = device.attach(process)

    def on_message(message, data):
        print(process, json.dumps(message, indent=2))

    scr = open("native.js").read().replace(
        "$process$", process
    )
    script = session.create_script(scr)
    script.on("message", on_message)
    script.load()
