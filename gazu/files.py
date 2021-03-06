from . import client


def all_output_types():
    """
    Return all output types list in database.
    """
    return client.fetch_all("output-types")


def get_output_type(output_type_id):
    """
    Return output type object corresponding to the given id.
    """
    return client.fetch_one("output-types", output_type_id)


def get_output_type_by_name(output_type_name):
    """
    Return software object corresponding to the given id.
    """
    result = client.fetch_all("output-types?name=%s" % output_type_name)
    return next(iter(result or []), None)


def get_output_file(output_file_id):
    """
    Returns the file corresponding to the given id.
    """
    path = "data/output-files/%s/" % (output_file_id)
    return client.get(path)


def get_output_files_for_entity(entity):
    """
    Retrieves all the outputs of a given asset
    """
    path = "data/output-files?entity_id=%s" % (entity["id"])
    return client.get(path)


def get_last_outputs_for_entity(entity):
    """
    Retrieves the last outputs of a given asset an store them by
    output_type

    :returns: the last outputs
    :rtype: dict
    """
    all_entity_outputs = get_output_files_for_entity(entity)
    last_entity_outputs = dict()
    for output in all_entity_outputs:
        if output['source_file'] is None:  # old cases
            continue
        key = output['output_type_id']
        if key not in last_entity_outputs.keys():
            last_entity_outputs[key] = output
            continue
        if last_entity_outputs[key]['revision'] < output['revision']:
            last_entity_outputs[key] = output
    return last_entity_outputs


def all_softwares():
    """
    Return all softwares listed in database.
    """
    return client.fetch_all("softwares")


def build_folder_path(
    task,
    name="main",
    mode="working",
    software=None,
    output_type=None,
    sep="/"
):
    """
    For a given task and options it returns the expected folder path.
    """
    data = {
        "mode": mode,
        "name": name,
        "sep": sep
    }
    if output_type is not None:
        data["output_type_id"] = output_type["id"]
    if software is not None:
        data["software_id"] = software["id"]

    result = client.post("data/tasks/%s/folder-path" % task["id"], data)
    return result["path"].replace(" ", "_")


def build_file_path(
    task,
    name="main",
    mode="working",
    software=None,
    output_type=None,
    comment="",
    version=1,
    sep="/"
):
    """
    For a given task and options, it returns the expected file path.
    """
    data = {
        "mode": mode,
        "name": name,
        "comment": comment,
        "version": version
    }
    if output_type is not None:
        data["output_type_id"] = output_type["id"]
    if software is not None:
        data["software_id"] = software["id"]

    result = client.post("data/tasks/%s/file-path" % task["id"], data)
    return "%s%s%s" % (
        result["path"].replace(" ", "_"),
        sep,
        result["name"].replace(" ", "_")
    )


def build_file_name(
    task,
    name="main",
    mode="working",
    software=None,
    output_type=None,
    comment="",
    version=1,
    sep="/"
):
    """
    For a given task and options, it returns the expected file name.
    """
    data = {
        "mode": mode,
        "name": name,
        "comment": comment,
        "version": version,
        "sep": sep
    }
    if output_type is not None:
        data["output_type_id"] = output_type["id"]
    if software is not None:
        data["software_id"] = software["id"]

    result = client.post("data/tasks/%s/file-path" % task["id"], data)
    return result["name"].replace(" ", "_")


def set_working_file_thumbnail(working_file, th_path):
    """
    Upload a thumbnail for given working file.
    """
    return client.upload("thumbnails/working-files/%s.png" % working_file["id"])


def new_working_file(
    task,
    name="main",
    mode="working",
    software=None,
    comment="",
    person=None,
    revision=0,
    sep="/"
):
    """
    Create a new working_file for given task. It generates and store the
    expected path for given task and options.
    """
    data = {
        "name": name,
        "comment": comment,
        "task_id": task["id"],
        "revision": revision
    }
    if person is not None:
        data["person_id"] = person["id"]
    if software is not None:
        data["software_id"] = software["id"]

    return client.post("data/tasks/%s/working-files/new" % task["id"], data)


def new_output_file(
    task,
    working_file,
    person,
    comment,
    output_type=None,
    revision=0,
    sep="/"
):
    path = "data/tasks/%s/working-files/%s/output-files/new" % (
        task["id"],
        working_file["id"]
    )

    data = {
        "person_id": person["id"],
        "comment": comment,
        "revision": revision,
        "separator": sep
    }
    if output_type is not None:
        data["output_type_id"] = output_type["id"],

    return client.post(path, data)


def get_next_output_revision(task, output_type, name="main"):
    """
    Generate next expected output revision for given task.
    """
    path = "data/tasks/%s/output-types/%s/next-revision" % (
        task["id"],
        output_type["id"]
    )

    data = {
        "name": name,
    }

    return client.post(path, data)["next_revision"]


def get_last_output_revision(task, output_type):
    """
    Generate last output revision for given task.
    """
    revision = get_next_output_revision(task, output_type)
    if revision != 1:
        revision -= 1
    return revision


def get_last_output_files(task):
    """
    Generate a dict of last output files. One working file entry for each
    output file type.
    """
    path = "data/tasks/%s/last-output-files" % task["id"]
    return client.get(path)


def get_working_files_for_task(task):
    """
    List of all working files related to given task.
    """
    path = "data/tasks/%s/working-files" % task["id"]
    return client.get(path)


def get_last_working_files(task):
    """
    Generate a dict of last working files. One working file entry for each
    working file name.
    """
    path = "data/tasks/%s/last-working-files" % task["id"]
    return client.get(path)


def get_last_working_file_revision(task, name="main"):
    """
    Get last revision stored in the API for given task and given file name.
    """
    path = "data/tasks/%s/last-working-files" % task["id"]
    working_files_dict = client.get(path)
    return working_files_dict.get(name, 0)


def get_software(software_id):
    """
    Return software object corresponding to given ID.
    """
    return client.fetch_one("softwares", software_id)


def get_working_file(workfile_id):
    """
    Return workfile object corresponding to given ID.
    """
    return client.fetch_one("working-files", workfile_id)


def get_software_by_name(software_name):
    """
    Return software object corresponding to given name.
    """
    softwares = client.fetch_all("softwares?name=%s" % software_name)
    if len(softwares) > 0:
        return softwares[0]
    else:
        return None


def update_modification_date(working_file):
    """
    Update modification date of given working file with current time (now).
    """
    return client.put(
        "/actions/working-files/%s/modified" % working_file['id'],
        {}
    )


def set_project_file_tree(project, file_tree_name):
    """
    Use given file tree to generate files for given project.
    """
    data = {"tree_name": file_tree_name}
    path = "actions/projects/%s/set-file-tree" % project["id"]
    return client.post(path, data)
