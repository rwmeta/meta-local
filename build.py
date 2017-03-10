import json
import logging
import os
import time
import urllib.request

import yaml
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

PAGE_PARAMS_KEYWORD = '+++\n'

os.chdir(os.path.dirname(__file__))
__DIR__ = os.getcwd() + "/"
SRC_DIR = __DIR__ + "src/"
BUILD_DIR = __DIR__ + "build/"


def write_build_file(filename, contentObject):
    with open(BUILD_DIR + filename, 'w') as f:
        out = json.dumps(contentObject, ensure_ascii=False, indent=2)
        f.write(out)


def build_configs():
    logging.info("Build configs...")
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
                                end_params_idx += 1
                                if line == PAGE_PARAMS_KEYWORD:
                                    break
                            params = yaml.load('\n'.join(lines[1:end_params_idx]))
                            print(u"params = %s" % str(params))
                            page.update(params)

                            print(u"page = %s" % str(page))
                            page['type'] = 'LEGO'
                            page['alias'] = 'p' + str(page['id'])
                            page['command'] = '\n'.join(lines[end_params_idx + 1:])
                            pages.append(page)
            app_conf['pages'] = pages

            write_build_file("app_conf_" + app_alias + ".json", app_conf)
        except yaml.YAMLError as exc:
            print(exc)
    logging.info("Build configs...OK")


if __name__ == "__main__":
    lastBuildIdx = -1


    class ChangeEventHandler(FileSystemEventHandler):
        buildIdx = 0

        def on_moved(self, event):
            super(ChangeEventHandler, self).on_moved(event)
            self.buildIdx += 1

        def on_created(self, event):
            super(ChangeEventHandler, self).on_created(event)
            self.buildIdx += 1

        def on_deleted(self, event):
            super(ChangeEventHandler, self).on_deleted(event)
            self.buildIdx += 1

        def on_modified(self, event):
            super(ChangeEventHandler, self).on_modified(event)
            self.buildIdx += 1


    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = ChangeEventHandler()
    observer = Observer()
    observer.schedule(event_handler, SRC_DIR, recursive=True)
    observer.start()
    try:
        while True:
            if event_handler.buildIdx > lastBuildIdx:
                lastBuildIdx = event_handler.buildIdx
                build_configs()
                with urllib.request.urlopen("http://localhost:8089/api/meta/dev/clear-cache") as f:
                    pass
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
