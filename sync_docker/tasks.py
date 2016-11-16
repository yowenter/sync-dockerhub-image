from app import docker_huey
from docker_image import DockerClient

@docker_huey.task(retries=6, retry_delay=30)
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
        for i, step in enumerate(self.steps):
            self.started = i+1
            step.start()


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
    def __init__(self,image_name):
        self.image_name = image_name
	
    def start(self):
        DockerClient.pull(self.image_name)




class PushStep(Step):
	def __init__(self,image_name):
        self.image_name = image_name

    def start(self):
        DockerClient.push(self.image_name)



class TagStep(Step):
	
    def __init__(self,src_image,dst_image):
        self.src_image = src_image
        self.dst_image = dst_image


    def start(self):
        DockerClient.tag(src_image,dst_image)



def create_sync_blue_print(src_image,dst_image):
    pull_step = PullStep(src_image)
    tag_step = TagStep(src_image,dst_image)
    push_step = PushStep(dst_image)

    return BluePrint('sync.{}.{}'.format(src_image,dst_image),[pull_step,tag_step,push_step])






