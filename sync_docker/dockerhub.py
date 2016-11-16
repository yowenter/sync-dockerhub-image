import re

import requests


class DockerHubClient(requests.Session):

	def __init__(self, registry_url=None):
		self.base_url = registry_url
		self._headers = {'Content-Type': 'application/json'}

	@staticmethod
	def authorize(www-authenticate,uid=None,pwd=None):
		# todo support basic auth
		auth_url = re.search('realm="(.*?)"', a).groups()[0]
		service = re.search('service="(.*?)"', a).groups()[0]
		scope = re.search('scope="(.*?)"', a).groups()[0]


		data = requests.get(auth_url, params={'service': service, 'scope': scope}).json()
		return data['token']



	def manifests(self, namespace, name,tag):
		url = self._url('/{}/{}/manifests/{}'.format(namespace,name,tag))
		return self._get(url)

	def tags(self, namespace, name):
		url = self._url('/{}/{}/tags/list'.format(namespace,name))
		return self._get(url)


	@classmethod(function)
	def parse_repo(repo):
		pass

	@classmethod
	def diff_repo(cls, a_repo, b_repo):
		pass


    def _url(self, path):
        return '{0}{1}'.format(self.base_url, path)

    def _post(self, url, **kwargs):
        return self.post(url, **self._set_default_params(kwargs))

    def _patch(self, url, **kwargs):
        return self.patch(url, **self._set_default_params(kwargs))

    def _get(self, url, **kwargs):
        return self.get(url, **self._set_default_params(kwargs))

    def _delete(self, url, **kwargs):
        return self.delete(url, **self._set_default_params(kwargs))

    def _result(self, response, json=True, binary=False):
        assert not (json and binary)
        self._raise_for_status(response)
        if json:
            result = response.json()
            return result
        if binary:
            return response.content
        return response.text


    def _raise_for_status(self,resp):
    	resp.raise_for_status()


    def _put(self, url, **kwargs):
        return self.put(url, **self._set_default_params(kwargs))

    def _patch(self, url, **kwargs):
        return self.patch(url, **self._set_default_params(kwargs))

    def _set_default_params(self, kwargs):
        """Prepare the kwargs for an HTTP request by inserting the timeout
        parameter, if not already present."""
        kwargs.setdefault('timeout', self._timeout)
        kwargs.setdefault('verify', False)
        kwargs.setdefault('headers', self._headers)
        return kwargs






