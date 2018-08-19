import json
import os

import Weblib

weblib = Weblib.Weblib()


class DataHandler:

    def __init__(self, resource_path):

        self._resources = ["armor", "weapons", "charms"]
        self._res_path = resource_path

    def prepare_data(self):
        """
        Run through all the necessary preparations for the data.
        """
        self._get_database()
        self._parse_armors()



    def should_get_data(self):
        """
        Looks up if all the necessary resource files are already saved to the 
        directory.

        Returns:
            Boolean value indicating whether the data should be fetched or not

        """
        
        for r in self._resources:
            resource_path = os.path.join(self._res_path,
                                         "raw_{}.json".format(r))
            if not os.path.exists(resource_path):
                return True
            print("No need to fetch {}".format(r))
        
        return False


    def get_resource(self, resource: str):
        """
        Fetches the given resource and saves it to the "resources" directory.
        The saved file will be named raw_<resource>.json.

        Args:
            resource (str): name of the resource to be gettened.

        Returns:
            Nothing

        """

        res_json = weblib.get(resource)
        save_path = os.path.join("palico-bot", "resources",
                                "raw_{}".format(resource))

        with open("{}.json".format(save_path), "w") as res_file:
            json.dump(res_json, res_file, indent=4)


    def _get_database(self):
        """
        Fetches the MHW database over REST API and saves it locally for easier
        access.

        Returns:
            Nothing

        """

        if self.should_get_data():
            for r in self._resources:
                self.get_resource(r)

        return


    def _parse_armors(self):
        """
        Reads through the raw armor data and parses it to be more convenient for
        queries. Saves the parsed data to its own file.

        Returns:
            Nothing
        """

        raw_armor_path = os.path.join(self._res_path, "raw_armor.json")
        if not os.path.exists(raw_armor_path):
            raise FileNotFoundError(
                "{} does not exist yet!".format(raw_armor_path))

        with open(raw_armor_path, "r") as armor_file:
            armors = json.load(armor_file)

        final_result = {}
        for a in armors:

            # Register the set object
            set_name = a["armorSet"]["name"]
            if set_name not in final_result:
                final_result[set_name] = {
                    "defense": {"base": 0,
                                "max": 0,
                                "augmented": 0},
                    "resistances": {"fire": 0,
                                    "water": 0,
                                    "ice": 0,
                                    "thunder": 0,
                                    "dragon": 0},
                    "skills": {},
                    "materials": {},
                    "rank": a["armorSet"]["rank"]
                }

            set_obj = final_result[set_name]

            new_piece = {
                "name": a["name"],
                "rarity": a["rarity"],
                "rank": a["rank"],
                "defense": a["defense"],
                "resistances": a["resistances"],
                "slots": a["slots"]
            }

            mats = []
            for m in a["crafting"]["materials"]:
                # Build a new material object without all the excess info
                mats.append({"quantity": m["quantity"],
                             "item": m["item"]["name"]})

            skills = []
            for s in a["skills"]:
                # Build a new skill object without all the excess info
                skills.append({"name": s["skillName"],
                               "level": s["level"]})

            new_piece["materials"] = mats
            new_piece["skills"] = skills

            # Add the piece to the set
            set_obj[a["type"]] = new_piece

            # Update the set totals
            for d in set_obj["defense"]:
                set_obj["defense"][d] += new_piece["defense"][d]

            for r in set_obj["resistances"]:
                set_obj["resistances"][r] += new_piece["resistances"][r]

            for m in mats:
                mn = m["item"]
                mq = m["quantity"]
                if mn in set_obj["materials"]:
                    set_obj["materials"][mn]["quantity"] += mq
                else:
                    set_obj["materials"][mn] = {"quantity": mq}

        # Write the parsed data to the file
        file_name = "parsed_armor.json"
        with open(os.path.join(self._res_path, file_name), "w") as f:
            json.dump(final_result, f, indent=4)

        return


        
