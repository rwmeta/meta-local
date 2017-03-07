import json
import os

import yaml

PAGE_PARAMS_KEYWORD = '+++\n'

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"
SRC_DIR = __DIR__ + "src/"
BUILD_DIR = __DIR__ + "build/"


def write_build_file(filename, contentObject):
    with open(BUILD_DIR + filename, 'w') as f:
        out = json.dumps(contentObject, ensure_ascii=False)
        f.write(out)


with open(SRC_DIR + "config.yml", 'r') as stream:
    try:
        conf = yaml.load(stream)
        write_build_file("main_conf.json", conf.get("main"))
        apps = conf.get("apps")
        write_build_file("main_part_conf.json", {
            "databases": conf.get("databases"),
            "apps": apps
        })

        app_alias = list(apps.keys())[0]
        app = apps[app_alias]
        app_conf = {}
        app_conf['app'] = app
        app_conf['actors'] = []
        app_conf['entities'] = {}
        app_conf['entityFields'] = []

        pages = []

        for root, subdirs, files in os.walk(SRC_DIR + "page"):
            for filename in files:
                file_path = os.path.join(root, filename)
                print(u"file_path = %s" % str(file_path))
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 0:
                        page = {
                            'role': 'PAGE',
                            'span': 12,
                            'boxed': True,
                            'embedded': False,
                            'unlisted': False,
                            'entity_id': 244,
                            'context_menu_action': 'none',
                            'in_list_for_developers': False,
                            'parent_ids': [],
                        }
                        end_params_idx = 0
                        if lines[0] != PAGE_PARAMS_KEYWORD:
                            raise AssertionError("Page should have params: \n+++\nkey = value\n+++\n")

                        for line in lines[1:]:
                            if line == PAGE_PARAMS_KEYWORD:
                                break
                            end_params_idx += 1
                        params = yaml.load('\n'.join(lines[1:end_params_idx]))
                        page.update(params)

                        page['type'] = 'LEGO'
                        page['alias'] = 'p' + str(page['id'])
                        page['command'] = '\n'.join(lines[end_params_idx:])
                        pages.append(page)
        app_conf['pages'] = pages

        write_build_file("app_conf_" + app_alias + ".json", app_conf)
    except yaml.YAMLError as exc:
        print(exc)
