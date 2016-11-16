import subprocess


class DockerClient:
    @staticmethod
    def pull(image_name):
        result = subprocess.call(["docker", "pull", image_name])
        if result != 0:
            raise Exception("pull image failure %s" % image_name)

    @staticmethod
    def push(image_name):
        result = subprocess.call(["docker", "push", image_name])
        if result != 0:
            raise Exception("push image failure %s" % image_name)

    @staticmethod
    def tag(src_image_name, dst_image_name):
        result = subprocess.call(
            ["docker", "tag", src_image_name, dst_image_name])
        if result != 0:
            raise Exception("tag image failure %s -> %s" % (src_image_name, dst_image_name))
