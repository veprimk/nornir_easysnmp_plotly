from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_config
# from easysnmp import snmp_get, snmp_set
from easysnmp import Session
from datetime import datetime
import time


def get_interface_stats(task, interface_dict):
    f = open(f'{task.host.hostname}_interface_{interface_dict["ifslug"]}.txt', 'a')
    session = Session(hostname=task.host.hostname, community='private', version=2)
    in_octets = session.get(f'.1.3.6.1.2.1.2.2.1.10.{interface_dict["ifindex"]}')
    out_octets = session.get(f'.1.3.6.1.2.1.2.2.1.16.{interface_dict["ifindex"]}')
    print(in_octets, out_octets) #Printing data just to make sure that it's running...
    f.write(f'{datetime.now().isoformat()},{interface_dict["ifname"]},{in_octets.value},{out_octets.value}\n')
    f.close()
    return [in_octets, out_octets]


def get_interface_utilization(interface_dict, interval, duration, host="all"):
    nr = InitNornir()
    if host != "all":
        nr = nr.filter(name=host)
    for i in range(int(duration/interval)):
        results = nr.run(task=get_interface_stats, interface_dict=interface_dict)
        time.sleep(interval)
    
    print_result(results)
        


def configure_snmp():
    nr = InitNornir()
    cfg = ['snmp-server community public RO', 'snmp-server community private RW']
    result = nr.run(
        task=netmiko_send_config,
        config_commands=cfg
        )
    print_result(result)



def main():
    # configure_snmp() # You can use this command to configure the snmp if not already done.
    interval = 5 # seconds
    duration = 300 # seconds
    interface_dict = {
        "ifindex": 8, # This is the index of the interface MIB
        "ifname": "GigabitEthernet0/7",
        "ifslug": "gi0_7"
    }

    get_interface_utilization(
        interface_dict=interface_dict,
        interval=interval,
        duration=duration
    )



if __name__ == "__main__":
    main()
