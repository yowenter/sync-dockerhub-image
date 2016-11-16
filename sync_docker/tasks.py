from app import docker_huey


@docker_huey.task(retries=6, retry_delay=30)
def sync_image():
    pass


class BluePrint(object):
    state = None
    started = 0

    def __init__(self, name=None, steps=None):

        self.name = name
        self.steps = steps

    def start(self):
        self.state = RUN

        for i, step in enumerate(self.steps):
            self.started = i+1
            step.start()


class Step(object):

    def start(self):
        pass


class PullStep(Step):
	pass



class PushStep(Step):
	pass



class TagStep(Step):
	pass


