import subprocess


class DockerClient:
    @staticmethod
    def pull(image_name):
        result = subprocess.call(["docker", "pull", image_name])
        return True if result == 0 else False

    @staticmethod
    def push(image_name):
        result = subprocess.call(["docker", "push", image_name])
        return True if result == 0 else False

    @staticmethod
    def tag(src_image_name, dst_image_name):
        result = subprocess.call(
            ["docker", "tag", src_image_name, dst_image_name])
        return True if result == 0 else False
