import asyncio
import discord
import json
import os

import Weblib

weblib = Weblib.Weblib()

armor_pieces = ["head", "waist", "chest", "legs", "gloves"]

weapons = ["greatsword", "longsword", "gunlance", "heavy-bowgun",
           "light-bowgun", "lance", "sword-and-shield",
           "charge-blade", "bow", "insect-glaive", "hammer",
           "dual-blades", "hunting-horn", "switch-axe"]

class DataHandler:

    _handler = None

    """
    Handles the data parsing and queries for the bot.
    """

    def __init__(self, resource_path, bot):
        """
        Constructor.

        Args:
            resource_path (str): path to the resource directory.
            bot (discord.commands.Bot): reference to the bot object.

        Returns:
            Nothing

        """

        self._resources = ["armor", "weapons", "charms", "skills"]
        self._res_path = resource_path
        self._bot = bot

        self._armors = None
        self._weapons = None
        self._charms = None
        self._skills = None
        DataHandler._handler = self

    @staticmethod
    def get_handler():
        if DataHandler._handler:
            return DataHandler._handler
        else:
            raise Exception("DataHandler not existing!")

    def prepare_data(self):
        """
        Run through all the necessary preparations for the data.
        """
        self._get_database()
        self._parse_armors()

    async def get_thing(self, thing, thing_type, rank):
        if thing_type == "set":
            await self.get_armor_set_info(thing, rank)
            return

        if thing_type in armor_pieces:
            pass

        if thing_type in weapons:
            pass

        return

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

    async def get_armor_set_info(self, set_name, rank=None):
        """
        Fetches the armor set information from the database.

        Args:
            set_name (str): name of the armor set to be queried.
            rank (str): high-rank or low-rank. Optional. If not given, both
                sets are returned.

        Returns:
            Dictionary containing the set information

        """

        set_name = set_name.lower()

        results = {}
        for set_key in self._armors.keys():
            # If rank not give, get add bish
            a_set = self._armors[set_key]
            if set_name in set_key.lower() and (rank == a_set["rank"] or rank is None):
                pieces = [a_set[piece]["name"] for piece in armor_pieces]

                results[set_key] = {"defense": a_set["defense"],
                                    "resistances": a_set["resistances"],
                                    "skills": a_set["skills"],
                                    "rank": a_set["rank"],
                                    "pieces": pieces
                                    }

        if not results:
            await self._bot.say("No results!")
            return

        for r in results:
            emb = discord.Embed(title=r,
                                description="{} rank set".format(results[r]["rank"].capitalize()))
            emb.add_field(name="Set pieces",
                          value="\n".join(results[r]["pieces"]))
            defs = list(str(value) for value in results[r]["defense"].values())
            emb.add_field(
                name="Defense",
                value="Base: {}\nMax: {}\nAugmented: {}".format(defs[0],
                                                                defs[1],
                                                                defs[2]))

            await self._bot.say(embed=emb)
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

        out_file = os.path.join(self._res_path, "parsed_armor.json")
        # If parsed_armor.json exists, load it and return
        if os.path.exists(out_file):
            with open(out_file, "r") as json_out:
                self._armors = json.load(json_out)
                return

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
            # TODO: Add slots to the set totals
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
        with open(out_file, "w") as f:
            json.dump(final_result, f, indent=4)

        self._armors = final_result

        return
