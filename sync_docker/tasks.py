import logging
from app import docker_huey
from docker_image import DockerClient

RUN = 'running'

LOG = logging.getLogger(__name__)


@docker_huey.task(retries=3, retry_delay=180)
def sync_image(blue_print):
    blue_print.start()


class BluePrint(object):
    state = None
    started = 0

    def __init__(self, name=None, steps=None):
        self.name = name
        self.steps = steps

    def start(self):
        self.state = RUN
        LOG.info("BluePrint %s started", self.steps)
        for i, step in enumerate(self.steps):
            self.started = i + 1
            step.start()
            LOG.debug("BluePrint step  %s, %s  ", step, i)


class Step(object):
    def start(self):
        pass

    def on_failure(self):
        # handle error, and make clean
        pass

    def on_succeed(self):
        # make clean 
        pass


class PullStep(Step):
    def __init__(self, image_name):
        self.image_name = image_name

    def start(self):
        DockerClient.pull(self.image_name)

    def __repr__(self):
        return "Pull Image %s " % self.image_name


class PushStep(Step):
    def __init__(self, image_name):
        self.image_name = image_name

    def start(self):
        DockerClient.push(self.image_name)

    def __repr__(self):
        return "Push Image %s " % self.image_name


class TagStep(Step):
    def __init__(self, src_image, dst_image):
        self.src_image = src_image
        self.dst_image = dst_image

    def start(self):
        DockerClient.tag(self.src_image, self.dst_image)

    def __repr__(self):
        return "Tag Image %s -> %s " % (self.src_image, self.dst_image)


class CleanStep(Step):
    def __init__(self, src_image, dst_image):
        self.src_image = src_image
        self.dst_image = dst_image

    def start(self):
        DockerClient.rmi(self.src_image)
        DockerClient.rmi(self.dst_image)

    def __repr__(self):
        return "Rmi Image %s , %s " % (self.src_image, self.dst_image)


def create_sync_blue_print(src_image, dst_image, need_clean=True):
    pull_step = PullStep(src_image)
    tag_step = TagStep(src_image, dst_image)
    push_step = PushStep(dst_image)
    if need_clean:
        clean_step = CleanStep(src_image, dst_image)
        return BluePrint('sync.{}.{}'.format(src_image, dst_image), [pull_step, tag_step, push_step, clean_step])
    else:
        return BluePrint('sync.{}.{}'.format(src_image, dst_image), [pull_step, tag_step, push_step])
