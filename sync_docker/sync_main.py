import logging
import requests
from huey import crontab
from app import docker_huey
from dockerhub import DockerHubClient
from settings import (LIBRARY_IMAGE_LIST_PATH,
                      DOCKER_REGISTRY_API,
                      TARGET_REGISTRY_API,
                      TARGET_REGISTRY,
                      THIRD_PARTY_LIST_PATH,
                      TARGET_THIRD_PARTY_NAMESPACE,
                      IMAGE_NAME_CONVERT_LIST_PATH)

from tasks import create_sync_blue_print, sync_image

LOG = logging.getLogger(__name__)


def read_from_file(fpath):
    with open(fpath, 'r') as f:
        lines = f.readlines()
        lines = map(lambda x: x.strip(), lines)
        lines = filter(lambda x: x and not x.startswith('#'), lines)
        return lines


def equal_manifests(a_manifests, b_manifests):
    a_fs_layers = a_manifests.get("fsLayers", [])
    b_fs_layers = b_manifests.get("fsLayers", [])

    if len(a_fs_layers) != len(b_fs_layers):
        return False

    for i in range(len(a_fs_layers)):
        if a_fs_layers[i] != b_fs_layers[i]:
            return False

    return True


def sync_image_from_dockerhub(image_name):
    _, namespace, name, _ = DockerHubClient.parse_repo(image_name)

    docker_hub_client = DockerHubClient(DOCKER_REGISTRY_API)
    tags = docker_hub_client.tags(namespace, name).get("tags", [])
    manifests = [docker_hub_client.manifests(namespace, name, tag) for tag in tags]
    tag_manifests = dict(zip(tags, manifests))

    target_docker_hub_client = DockerHubClient(TARGET_REGISTRY_API)

    target_namespace, target_name = _convert_image(image_name)
    LOG.info("src_image: %s/%s, target_image: %s/%s", namespace, name, target_namespace, target_name)
    if target_namespace != 'library' and target_namespace != TARGET_THIRD_PARTY_NAMESPACE:
        LOG.warning("third party image %s has no namespace", image_name)
        return

    try:
        target_tags = target_docker_hub_client.tags(target_namespace, target_name).get("tags", []) or []
    except  requests.exceptions.HTTPError as e:
        target_tags = []

    target_manifests = [target_docker_hub_client.manifests(target_namespace, target_name, tag) for tag in target_tags]
    target_tag_manifests = dict(zip(target_tags, target_manifests))

    new_add_tags = set(tags) - set(target_tags)
    new_updated_tags = set()

    need_compare_tags = set(tags) & set(target_tags)

    for tag in need_compare_tags:
        a_tag_manifests = tag_manifests.get(tag, {})
        b_tag_manifests = target_tag_manifests.get(tag, {})

        if not equal_manifests(a_tag_manifests, b_tag_manifests):
            new_updated_tags.add(tag)
    LOG.info("Update Image %s/%s , tags:%s", target_namespace, target_name, list(new_add_tags | new_updated_tags))
    for update_tag in list(new_add_tags | new_updated_tags):
        src_image = "{}:{}".format(name, update_tag) if namespace == 'library' else "{}/{}:{}".format(namespace, name,
                                                                                                      update_tag)
        dst_image = "{}/{}/{}:{}".format(TARGET_REGISTRY, target_namespace, target_name, update_tag)
        blueprint = create_sync_blue_print(src_image, dst_image, need_clean=namespace != 'library')
        sync_image(blueprint)

        if namespace == 'library':
            dst_image_2 = "{}/{}:{}".format(TARGET_REGISTRY, target_name, update_tag)
            blueprint2 = create_sync_blue_print(src_image, dst_image_2, need_clean=False)
            sync_image(blueprint2)


def _load_image_name_convert_dict():
    data = {}
    with open(IMAGE_NAME_CONVERT_LIST_PATH, "r") as f:
        for line in f:
            k, v = line.strip().split("->")
            data[k.strip()] = v.strip()
    return data


image_name_convert_dict = _load_image_name_convert_dict()


def _convert_image(image_name):
    '''

    :param image_name: library/ubuntu -> library ubuntu
                        tutum/ubuntu -> {TARGET_THIRD_NAMESPACE} ubuntu
    :return:
    '''
    _, namespace, name, _ = DockerHubClient.parse_repo(image_name)

    if namespace == 'library':
        return namespace, name

    else:
        dst_image_name = image_name_convert_dict.get("{}/{}".format(namespace, name)) or "{}/{}".format(namespace, name)

        _, namespace, name, _ = DockerHubClient.parse_repo(dst_image_name)
        return namespace, name


@docker_huey.periodic_task(crontab(hour=0))
def sync_all_library_images():
    image_list = read_from_file(LIBRARY_IMAGE_LIST_PATH)
    for image_name in image_list:
        try:
            sync_image_from_dockerhub(image_name)
        except:
            LOG.error("Create sync library image task failure .%s ", image_name, exc_info=True)


@docker_huey.periodic_task(crontab(hour=20))
def sync_all_third_party_images():
    third_party_image_list = read_from_file(THIRD_PARTY_LIST_PATH)
    for image_name in third_party_image_list:
        try:
            sync_image_from_dockerhub(image_name)
        except:
            LOG.error("Create sync third party image task failure .%s ", image_name, exc_info=True)


def test_create():
    blueprint = create_sync_blue_print('ubuntu:14.04', '10.1.4.167:5000/library/ubuntu:latest')
    sync_image(blueprint)
    LOG.info("test sync image %s", blueprint)


if __name__ == '__main__':
    # sync_all_library_images()
    # test_create()
    sync_all_third_party_images()
