from jinja2 import Template, FileSystemLoader, Environment
from pathlib import Path


async def process():
    template = """hostname {{ hostname }}

no ip domain lookup
ip domain name local.lab
ip name-server {{ name_server_pri }}
ip name-server {{ name_server_sec }}

ntp server {{ ntp_server_pri }} prefer
ntp server {{ ntp_server_sec }}"""

    data = {
        "hostname": "core-sw-waw-01",
        "name_server_pri": "1.1.1.1",
        "name_server_sec": "8.8.8.8",
        "ntp_server_pri": "0.pool.ntp.org",
        "ntp_server_sec": "1.pool.ntp.org",
    }

    p = Path(__file__).parent.parent / 'templates'  # sample relative path
    template_loader = FileSystemLoader(searchpath="../templates")
    template_env = Environment(loader=template_loader)
    template = template_env.get_template('index.html')
    schedule_template = Template(template, enable_async=True)

    return await schedule_template.render_async(data)
