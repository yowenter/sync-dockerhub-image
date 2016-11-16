import logging
import requests
from dockerhub import DockerHubClient
from settings import LIBRARY_IMAGE_LIST_PATH, DOCKER_REGISTRY_API, TARGET_REGISTRY_API, TARGET_REGISTRY_ENDPOINT
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


def sync_library():
    library_images = read_from_file(LIBRARY_IMAGE_LIST_PATH)
    for image in library_images:
        endpoint, namespace, name, tag = DockerHubClient.parse_repo(image)

        docker_hub_client = DockerHubClient(DOCKER_REGISTRY_API)
        tags = docker_hub_client.tags(namespace, name).get("tags", [])
        manifests = [docker_hub_client.manifests(namespace, name, tag) for tag in tags]
        tag_manifests = dict(zip(tags, manifests))

        target_docker_hub_client = DockerHubClient(TARGET_REGISTRY_API)
        try:
            target_tags = target_docker_hub_client.tags(namespace, name).get("tags", [])
        except  requests.exceptions.HTTPError as e:
            target_tags = []

        target_manifests = [docker_hub_client.manifests(namespace, name, tag) for tag in target_tags]
        target_tag_manifests = dict(zip(target_tags, target_manifests))

        new_add_tags = set(tags) - set(target_tags)
        new_updated_tags = set()

        need_compare_tags = set(tags) & set(target_tags)

        for tag in need_compare_tags:
            a_tag_manifests = tag_manifests.get(tag, {})
            b_tag_manifests = target_tag_manifests.get(tag, {})

            if not equal_manifests(a_tag_manifests, b_tag_manifests):
                new_updated_tags.add(tag)

        for update_tag in list(new_add_tags | new_updated_tags):
            src_image = "{}:{}".format(name, update_tag)
            dst_image = "{}/library/{}:{}".format(TARGET_REGISTRY_ENDPOINT, name, update_tag)
            dst_image_2 = "{}/{}:{}".format(TARGET_REGISTRY_ENDPOINT, name, update_tag)
            blueprint = create_sync_blue_print(src_image, dst_image)
            blueprint2 = create_sync_blue_print(src_image, dst_image_2)
            sync_image(blueprint)
            sync_image(blueprint2)


def test_create():
    blueprint = create_sync_blue_print('ubuntu:14.04', '10.1.4.167:5000/library/ubuntu:latest')
    sync_image(blueprint)
    LOG.info("test sync image %s", blueprint)


if __name__ == '__main__':
    test_create()
