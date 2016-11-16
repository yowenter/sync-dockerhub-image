import re

import requests


class DockerHubClient(requests.Session):
    def __init__(self, registry_url=None, timeout=30):
        self.base_url = registry_url
        self._headers = {'Content-Type': 'application/json'}
        self._timeout = timeout
        super(DockerHubClient, self).__init__()

    @staticmethod
    def authorize(www_authenticate, uid=None, pwd=None):
        # todo support basic auth
        auth_url = re.search('realm="(.*?)"', www_authenticate).groups()[0]
        service = re.search('service="(.*?)"', www_authenticate).groups()[0]
        scope = re.search('scope="(.*?)"', www_authenticate).groups()[0]

        data = requests.get(
            auth_url, params={'service': service, 'scope': scope}).json()
        return data['token']

    def manifests(self, namespace, name, tag, retried=0):
        url = self._url('/{}/{}/manifests/{}'.format(namespace, name, tag))
        response = self._get(url)
        if response.headers.get('www-authenticate') and response.status_code == 401 and retried < 4:
            token = self.authorize(response.headers['www-authenticate'])
            self._headers.update({'Authorization': "Bearer {}".format(token)})
            return self.manifests(namespace, name, tag, retried + 1)
        return self._result(response)

    def tags(self, namespace, name, retried=0):
        url = self._url('/{}/{}/tags/list'.format(namespace, name))
        response = self._get(url)
        if response.headers.get('www-authenticate') and response.status_code == 401 and retried < 4:
            token = self.authorize(response.headers['www-authenticate'])
            self._headers.update({'Authorization': "Bearer {}".format(token)})
            return self.tags(namespace, name, retried + 1)
        return self._result(response)

    @classmethod
    def parse_repo(cls, repo):
        repo = repo.strip()
        tag = None
        if len(repo.split(':')) == 2:
            image, tag = repo.split(":")
        else:
            image = repo

        if len(image.split('/')) == 3:
            endpoint, namespace, name = image.split('/')
        elif len(image.split('/')) == 2:
            endpoint = None
            namespace, name = image.split('/')

        else:
            name = image
            namespace = 'library'
            endpoint = None

        return endpoint, namespace, name, tag

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

    def _raise_for_status(self, resp):
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
