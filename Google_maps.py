def find_path_city_a_b(city,origin,destination):
    """
    route JSON example at:
    https://maps.googleapis.com/maps/api/directions/json?origin=Centrum,Warsaw,Poland&destination=Plac+Zbawiciela,Warsaw,Poland&mode=transit
    """
    import requests

    url="https://maps.googleapis.com/maps/api/directions/json?origin="+origin+","+city+",Poland&destination="+destination+","+city+",Poland&mode=transit"

    #url="https://maps.googleapis.com/maps/api/directions/json?origin=adajdhfgdsg&destination=Plac+Zbawiciela,Warsaw,Poland&mode=transit"


    google_maps_raw=requests.get(url)
    google_maps_json=google_maps_raw.json()

    all_instructions="Your instructions are:\t"

    if google_maps_json["geocoded_waypoints"][0]["geocoder_status"]=="OK":
        step_number=0
        steps_amount=len(google_maps_json["routes"][0]["legs"][0]["steps"])

        while(step_number<steps_amount):
            for item in google_maps_json["routes"][0]["legs"][0]["steps"][step_number]:
                if item=="html_instructions":
                    instruction=google_maps_json["routes"][0]["legs"][0]["steps"][step_number]["html_instructions"].lower()
                    path=google_maps_json["routes"][0]["legs"][0]["steps"][step_number]
                    if "walk" in instruction:
                        all_instructions = all_instructions + "\n" + path["html_instructions"]+""+"("+path["distance"]["text"]+")"
                    elif "tram" in instruction or "bus" in instruction or "subway" in instruction:
                        all_instructions = all_instructions + "\n" + path["html_instructions"]
                        all_instructions = all_instructions + "\n" + "\tLine: "+path["transit_details"]["line"]["short_name"]
                        all_instructions = all_instructions + "\n" + "\tFrom: "+path["transit_details"]["departure_stop"]["name"]
                        all_instructions = all_instructions + "\n" + "\tTo: "+path["transit_details"]["arrival_stop"]["name"]
                    else:
                        print (instruction)
            step_number=step_number+1
    else:
        return ("ERROR: Unknown location: \nCity: \"" + city + "\"\nOrigin: \"" + origin + "\"\nDestination: \"" + destination +"\"" )

    return (all_instructions)

    #for item in google_maps_json["geocoded_waypoints"][0]["geocoder_status"]:
    #    print (item)
