tree_shape = {
    "ROOT": {
        "tag": "",
        "children": ["ACRONYM", "ACRONYM_LOWER"]
    },
    "ACRONYM": {
        "tag": "",
        "children": ["SEASON_FL_LOWER", "SEASON_FL_UPPER", "SEASON", "SEASON_UPPER", "SEASON_CAPITALIZED", "YEAR", "GEORGIAN_YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "ACRONYM_LOWER": {
        "tag": "",
        "children": ["SEASON_FL_LOWER", "SEASON_FL_UPPER", "SEASON", "SEASON_UPPER", "SEASON_CAPITALIZED", "YEAR", "GEORGIAN_YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON_FL_LOWER": {
        "tag": "",
        "children": ["YEAR", "GEORGIAN_YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON_FL_UPPER": {
        "tag": "",
        "children": ["YEAR", "GEORGIAN_YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON": {
        "tag": "",
        "children": ["YEAR", "GEORGIAN_YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON_CAPITALIZED": {
        "tag": "",
        "children": ["YEAR", "GEORGIAN_YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON_UPPER": {
        "tag": "",
        "children": ["YEAR", "GEORGIAN_YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "YEAR": {
        "tag": "",
        "children": ["SEASON_FL_LOWER", "SEASON_FL_UPPER", "SEASON", "SEASON_UPPER", "SEASON_CAPITALIZED", "NOTHING"]
    },
    "GEORGIAN_YEAR": {
        "tag": "",
        "children": ["SEASON_FL_LOWER", "SEASON_FL_UPPER", "SEASON", "SEASON_UPPER", "SEASON_CAPITALIZED", "NOTHING"]
    },
    "SEMESTER_YEAR": {
        "tag": "",
        "children": ["SEMESTER_NO", "SEMESTER_NEXT_YEAR", "NOTHING"]
    },
    "SEMESTER_NEXT_YEAR": {
        "tag": "",
        "children": ["NOTHING"]
    },
    "SEMESTER_NO": {
        "tag": "",
        "children": ["SEASON_FL_LOWER", "SEASON_FL_UPPER", "SEASON", "SEASON_UPPER", "SEASON_CAPITALIZED", "NOTHING"]
    },
    "NOTHING": {
        "tag": "",
        "children": [],
        "leaf_mark": True
    }
}

def keyword_values(key):
    values = []
    _keyword = key["keyword"]
    if "FIRST" in key["capitalizable_letters"]:
        values.append(_keyword.capitalize())
    if "ALL" in key["capitalizable_letters"]:
        values.append(_keyword.upper())
    if "NONE" in key["capitalizable_letters"]:
        values.append(_keyword.lower())
    return values

class KeywordTree:

    def __init__(self, course_info, additional_keywords):
        self.tree = {}
        self.course_info = course_info
        self.additional_keywords = additional_keywords if additional_keywords != None else []
        self.key_list = []
        self.__build_keyword_tree()

    def __fill_tree_tags(self):
        tree_shape["ACRONYM"]["tag"] = self.course_info["acronym"].upper()
        tree_shape["ACRONYM_LOWER"]["tag"] = self.course_info["acronym"].lower()
    #    tree_shape["FULL_NAME"]["tag"] = self.course_info["course_name"].replace(" ", "")

        tree_shape["SEASON_FL_LOWER"]["tag"] = self.course_info["season"][0].lower()
        tree_shape["SEASON_FL_UPPER"]["tag"] = self.course_info["season"][0].upper()

        tree_shape["SEASON"]["tag"] = self.course_info["season"].lower()
        tree_shape["SEASON_UPPER"]["tag"] = self.course_info["season"].upper()
        tree_shape["SEASON_CAPITALIZED"]["tag"] = self.course_info["season"].capitalize()

        tree_shape["YEAR"]["tag"] = self.course_info["year"]
        tree_shape["GEORGIAN_YEAR"]["tag"] = str(int('13' + self.course_info["year"]) + 621)
        
        tree_shape["SEMESTER_YEAR"]["tag"] = self.course_info["semester_year"]
        tree_shape["SEMESTER_NEXT_YEAR"]["tag"] = str(int(self.course_info["semester_year"]) + 1)
        tree_shape["SEMESTER_NO"]["tag"] = self.course_info["semester_no"]

        for key in self.additional_keywords:
            all_keywords = keyword_values(key)

            for keyword in all_keywords:
                tree_shape[keyword] = {
                    "tag": keyword,
                    "children": [],
                }
                if key["order"] == 1:
                    tree_shape["ROOT"]["children"].append(keyword)
            
                for possible_child in self.additional_keywords:
                    if possible_child["order"] == key["order"]  + 1:
                        tree_shape[keyword]["children"].extend(keyword_values(possible_child))

                if key["is_last"]:
                    tree_shape[keyword]["children"] = ["SEASON_FL_LOWER", "SEASON_FL_UPPER", "SEASON", "SEASON_UPPER", "SEASON_CAPITALIZED", "YEAR", "GEORGIAN_YEAR", "SEMESTER_YEAR", "NOTHING"]


    def __add_special_char_nodes(self, node):
        if node["special_char_type"] == "dash":
            node["children"] = [
                {
                    "tag": "-",
                    "special_char_type": "dash",
                    "children": [],
                    "is_leaf": False
                },
                {
                    "tag": "",
                    "special_char_type": "dash",
                    "children": [],
                    "is_leaf": False
                }
            ]
        elif node["special_char_type"] == "underline":
            node["children"] = [
                {
                    "tag": "_",
                    "special_char_type": "underline",
                    "children": [],
                    "is_leaf": False
                },
                {
                    "tag": "",
                    "special_char_type": "underline",
                    "children": [],
                    "is_leaf": False
                }
            ]
        elif node["special_char_type"] == "any":
            node["children"] = [
                {
                    "tag": "-",
                    "special_char_type": "dash",
                    "children": [],
                    "is_leaf": False
                },
                {
                    "tag": "_",
                    "special_char_type": "underline",
                    "children": [],
                    "is_leaf": False
                },
                {
                    "tag": "",
                    "special_char_type": "any",
                    "children": [],
                    "is_leaf": False
                }
            ]

    def __build_node(self, shape_node, node, depth= 0):
        if depth > 3: return
        for child in shape_node["children"]:
            if "leaf_mark" in tree_shape[child] and node["tag"] != "": continue
            new_node = {"tag": tree_shape[child]["tag"], "children": [], "special_char_type": node["special_char_type"], "is_leaf": "leaf_mark" in tree_shape[child]}
            node["children"].append(new_node)
            self.__add_special_char_nodes(new_node)
            for special_char_child in new_node["children"]:
                self.__build_node(tree_shape[child], special_char_child, depth + 1)

    def __build_tree(self):
        self.tree = {"tag": "", "children": [], "special_char_type": "any", "is_leaf": False}
        shape_node = tree_shape["ROOT"]
        self.__build_node(shape_node, self.tree)

    def __traverse_tree(self, node, tags, depth):
        if node["is_leaf"]:
            self.key_list.append(tags)
            return

        for child in node["children"]:
            self.__traverse_tree(child, tags + child["tag"], depth + 1)

    def __build_keyword_tree(self):
        self.__fill_tree_tags()
        self.__build_tree()
        self.__traverse_tree(self.tree, "", 0)

    def gen_key_list(self):
        self.key_list.clear()
        self.__traverse_tree(self.tree, "", 0)
        return self.key_list