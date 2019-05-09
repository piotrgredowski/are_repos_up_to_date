import os

from lib import utils

curr_dir = os.path.dirname(os.path.realpath(__file__))

CONSTS = utils.read_yaml_file(os.path.join(curr_dir, 'consts.yaml'))


def main():
    template = utils.load_template(CONSTS.get('service_template_path'))

    path_to_script = os.path.join(curr_dir, CONSTS.get('main_script_name'))
    path_to_repos_list_file = os.path.join(curr_dir, CONSTS.get('repos_list_filename'))
    username = utils.get_username()
    display = utils.get_display()
    user_uid = utils.get_uid()

    rendered = template.render(
        path_to_script=path_to_script,
        path_to_repos_list_file=path_to_repos_list_file,
        username=username,
        display=display,
        user_uid=user_uid
    )

    utils.save_to_file(rendered, CONSTS.get('service_rendered_path'))


if __name__ == "__main__":
    main()
