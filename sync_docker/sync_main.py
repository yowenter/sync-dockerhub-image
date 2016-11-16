

from dockerhub import DockerHubClient


from settings import LIBRARY_IMAGE_LIST_PATH



def read_from_file(fpath):
	with open(fpath,'r') as f:
		lines = f.readlines()
		lines = map(lambda x:x.strip(),lines)
		lines = filter(lambda x:x and not x.startswith('#'),lines)
		return lines




def main():
	library_images = read_from_file(LIBRARY_IMAGE_LIST_PATH)
	for image in library_images:
		endpoint,namespace,name = DockerHubClient.parse_repo(image)

		docker_hub_client = DockerHubClient()
		tags = docker_hub_client.tags(namespace,name)

		for tag in tags:
			if DockerHubClient.diff_repo():
				pass

				








