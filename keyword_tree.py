tree_shape = {
    "ROOT": {
        "tag": "",
        "children": ["ACRONYM", "ACRONYM_LOWER"]
    },
    "ACRONYM": {
        "tag": "",
        "children": ["SEASON_FL_LOWER", "SEASON_FL_UPPER", "SEASON", "SEASON_UPPER", "SEASON_CAPITALIZED", "YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "ACRONYM_LOWER": {
        "tag": "",
        "children": ["SEASON_FL_LOWER", "SEASON_FL_UPPER", "SEASON", "SEASON_UPPER", "SEASON_CAPITALIZED", "YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON_FL_LOWER": {
        "tag": "",
        "children": ["YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON_FL_UPPER": {
        "tag": "",
        "children": ["YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON": {
        "tag": "",
        "children": ["YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON_CAPITALIZED": {
        "tag": "",
        "children": ["YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "SEASON_UPPER": {
        "tag": "",
        "children": ["YEAR", "SEMESTER_YEAR", "NOTHING"]
    },
    "YEAR": {
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

  
class KeywordTree:

    def __init__(self, course_info):
        self.tree = {}
        self.course_info = course_info
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
        tree_shape["SEMESTER_YEAR"]["tag"] = self.course_info["semester_year"]
        tree_shape["SEMESTER_NEXT_YEAR"]["tag"] = str(int(self.course_info["semester_year"]) + 1)
        tree_shape["SEMESTER_NO"]["tag"] = self.course_info["semester_no"]

    def __add_special_char_nodes(self, node):
        node["children"] = [
            {
                "tag": "_",
                "children": [],
                "is_leaf": False
            },
            {
                "tag": "-",
                "children": [],
                "is_leaf": False
            },
            {
                "tag": "",
                "children": [],
                "is_leaf": False
            }
        ]

    def __build_node(self, shape_node, node, depth= 0):
        if depth > 3: return
        for child in shape_node["children"]:
            if "leaf_mark" in tree_shape[child] and node["tag"] != "": continue
            new_node = {"tag": tree_shape[child]["tag"], "children": [], "is_leaf": "leaf_mark" in tree_shape[child]}
            node["children"].append(new_node)
            self.__add_special_char_nodes(new_node)
            for special_char_child in new_node["children"]:
                self.__build_node(tree_shape[child], special_char_child, depth + 1)

    def __build_tree(self):
        self.tree = {"tag": "", "children": [], "is_leaf": False}
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