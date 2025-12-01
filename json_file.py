import json

def safe_get(d, key, default="Not available"):
    return d.get(key, default) if isinstance(d, dict) else default

try:
    with open("intf.json") as f:
        data = json.load(f)

    interfaces = safe_get(data.get("data", {}), "openconfig-interfaces:interfaces")
    interface_list = safe_get(interfaces, "interface", [])

    if not interface_list:
        print("No interface data found")
        exit()

    intf = interface_list[0]

    name = safe_get(intf, "name")
    state = safe_get(intf, "state")
    intf_type = safe_get(state, "type")

  
    subifs = safe_get(intf, "subinterfaces")
    subif_list = safe_get(subifs, "subinterface", [])

    ipv4_address = "Not available"
    prefix_length = "Not available"

    if subif_list:
        subif0 = subif_list[0]

        ipv4 = safe_get(subif0, "openconfig-if-ip:ipv4")
        addresses = safe_get(ipv4, "addresses")
        addr_list = safe_get(addresses, "address", [])

        if addr_list:
            first_addr = addr_list[0]
            ipv4_address = safe_get(first_addr, "ip")
            state_v4 = safe_get(first_addr, "state")
            prefix_length = safe_get(state_v4, "prefix-length")

 
    counters = safe_get(state, "counters")
    in_octets = safe_get(counters, "in-octets")
    in_unicast = safe_get(counters, "in-unicast-pkts")
    out_octets = safe_get(counters, "out-octets")
    out_unicast = safe_get(counters, "out-unicast-pkts")

    print("name :", name)
    print("type:", intf_type)
    print("IPv4 address:", ipv4_address)
    print("Prefix length:", prefix_length)
    print("in octets:", in_octets)
    print("in unicast pkts:", in_unicast)
    print("out octets:", out_octets)
    print("out unicast pkts:", out_unicast)

except Exception as e:
    print("Error:", e)
